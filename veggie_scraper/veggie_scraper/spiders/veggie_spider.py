from scrapy import Spider, Request
from veggie_scraper.items import PostItem, ThreadItem, UserItem
from scrapy.selector import Selector
import re

class VeggieSpider(Spider):
    name = 'veggie_scraper'
    allowed_urls = ['http://www.veggieboards.com/forum/']
    start_urls = ['http://www.veggieboards.com/forum/11-vegetarian-support-forum/',
                  'http://www.veggieboards.com/forum/60-vegan-support-forum/',
                  'http://www.veggieboards.com/forum/188-raw-food-support-forum/']

    def parse(self, response):
        last_link = response.xpath('//div[@id="fixed-controls"]//a[@class="smallfont"]/@href')[-1].extract()
        base_link = last_link[:last_link.find('index')]
        last_page = last_link[last_link.find('index')+5:]
        last_page = last_page[:last_page.find('.')]

        post_list = response.xpath('//a[@class="thread_title_link"]/@href').extract()

        #filter out any sponsored redirect links
        post_list = [link for link in post_list if "misc.php" not in link]

        for i in range(2, last_page+1):
            yield Request(base_link + "index" + str(i) + ".html", callback=self.parse_page)

        for post in post_list:
            yield Request(post, callback=self.parse_post)

    def parse_page(self, response):
        post_list = response.xpath('//a[@class="thread_title_link"]/@href').extract()
        post_list = [link for link in post_list if "misc.php" not in link]

        for post in post_list:
            yield Request(post, callback=self.parse_post)

    def parse_post(self, response):
        pass