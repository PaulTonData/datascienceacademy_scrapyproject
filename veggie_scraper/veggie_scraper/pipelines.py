# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from veggie_scraper.items import PostItem, ThreadItem, UserItem
import logging
import pymongo

class MongoPipeline(object):

    post_collection = 'veggie_posts'
    thread_collection = 'threads'
    user_collection = 'users'
    
    def __init__(self, mongo_uri, mongo_db, mongo_user, mongo_pwd):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_user = mongo_user
        self.mongo_pwd = mongo_pwd

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_user=crawler.settings.get('MONGO_USER'),
            mongo_pwd=crawler.settings.get('MONGO_PWD')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(username=self.mongo_user, password=self.mongo_pwd)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if type(item) is PostItem:
            self.db[self.post_collection].insert(dict(item))
            logging.debug("Added Post Item to db")
            print(item['thread_id'] + ", " + item['post_num'] + ", " + item['user_id'])
        elif type(item) is ThreadItem:
            self.db[self.thread_collection].insert(dict(item))
            logging.debug("Added Thread Item to db")
            print(item['url'] + ", " + item['thread_id'])
        elif type(item) is UserItem:
            self.db[self.user_collection].insert(dict(item))
            logging.debug("Added User Item to db")
        return item
