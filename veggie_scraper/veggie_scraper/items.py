# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class PostItem(Item):
    forum_id = Field()
    thread_id = Field()
    user_id = Field()
    post_id = Field()
    text = Field()
    datetime = Field()

class ThreadItem(Item):
    thread_id = Field()
    url = Field()
    title = Field()

class UserItem(Item):
    user_id = Field()
    name = Field()
    join_date = Field()
    post_ct = Field()
    location = Field()
