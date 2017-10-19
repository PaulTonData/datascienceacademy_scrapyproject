# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class PostItem(Item):
    thread_id = Field()
    user_id = Field()
    post_id = Field()
    post_num = Field()
    text = Field()
    datetime = Field()

class ThreadItem(Item):
    url = Field()
    title = Field()
    thread_id = Field()
    forum = Field()

class UserItem(Item):
    user_id = Field()
    user_url = Field()