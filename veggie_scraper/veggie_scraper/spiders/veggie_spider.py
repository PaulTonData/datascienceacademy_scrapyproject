from scrapy import Spider, Request
from veggie_scraper.items import PostItem, ThreadItem, UserItem
from scrapy.selector import Selector
import re
import logging

class VeggieThreadSpider(Spider):
    name = 'veggie_thread_spider'
    allowed_urls = ['http://www.veggieboards.com/forum/']
    start_urls = ['http://www.veggieboards.com/forum/11-vegetarian-support-forum/']

    def parse(self, response):
        logging.debug("parsing post: " + response.url)

        #Use this to get the list of URLS
        last_link = response.xpath('//div[@id="fixed-controls"]//a[@class="smallfont"]/@href')[-1].extract()
        base_link = last_link[:last_link.find('index')]
        last_page = last_link[last_link.find('index')+5:]
        last_page = last_page[:last_page.find('.')]

        yield from self.parse_page(response)

        for i in range(2, int(last_page) + 1):
            next_url = base_link + "index" + str(i) + ".html"
            logging.debug("requesting next: " + next_url)
            yield Request(next_url, callback=self.parse_page)

    def parse_page(self, response):
        print("parsing current page: " + response.url)

        post_list = response.xpath('//a[@class="thread_title_link"]/@href').extract()

        #filter out any sponsored redirect links     
        post_list = [link for link in post_list if "misc.php" not in link]

        forum = response.url[34:]
        forum = forum[:forum.find('/')]

        for post in post_list:
            #build ThreadItem
            item = ThreadItem()
            item['url'] = post

            title = post[post.find(forum) + len(forum) + 1:]
            item['title'] = title
            item['thread_id'] = title[:title.find('-')]
            item['forum'] = forum

            #yield ThreadItem
            yield item

            #go into post and gather comments
            #yield Request(post, callback=self.parse_post)


class VeggieSpider(Spider):
    name = 'veggie_spider'
    allowed_urls = ['http://www.veggieboards.com/forum/']
    #read in pre-scraped URLS
    with open('vegetarian_threads.txt', 'r') as f:
        start_urls = [url.strip() for url in f.readlines()]
        start_urls = start_urls[1000:]

    def parse(self, response):
        logging.debug("parsing post: " + response.url)
        yield from self.parse_post(response)

    def parse_post(self, response):
        yield from self.parse_post_page(response)

        #check if multi-page thread, if so, build links and loop
        base_link = response.url[:-5]
        last_link = response.xpath('//div[@class="pagenav"]//a[starts-with(@title, "Last")]/@href').extract_first()
        if last_link:
            last_page = last_link[len(base_link) + 1:-5]
            logging.debug("multi-page thread! last link on this page is: " + last_page)
            for i in range(2, int(last_page) + 1):
                yield Request(base_link + "-" + str(i) + ".html", callback=self.parse_post_page)

    def parse_post_page(self, response):
        logging.debug("parsing post page: " + response.url)
        base_link = response.url
        #'http://www.veggieboards.com/forum/11-vegetarian-support-forum/225682-almonds-nuts.html'

        tail = base_link[34:-5]
        #11-vegetarian-support-forum/225682-almonds-nuts

        thread = tail[tail.find('/') + 1:]
        #225682-almonds-nuts

        thread_id = thread[:thread.find('-')]
        #225682

        comments = response.xpath('//section[contains(@id, "post")]')

        for comment in comments:
            user = comment.xpath('.//a[@class="bigusername"]//text()').extract_first()
            post_id = comment.xpath('.//div[starts-with(@id, "post_message")]/@id').extract_first()
            post_id = post_id[13:]
            post_num = comment.xpath('.//span[@class="post-count"]/a//text()').extract_first()
            text = comment.xpath('.//div[starts-with(@id, "post_message")]').extract_first()
            datetime = comment.xpath('.//span[@itemprop="dateCreated"]/text()').extract_first()

            item = PostItem()
            item['thread_id'] = thread_id
            item['user_id'] = user
            item['post_id'] = post_id
            item['post_num'] = post_num
            item['text'] = text
            item['datetime'] = datetime

            yield item
