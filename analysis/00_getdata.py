from pymongo import MongoClient
import json

user = '*****'
pwd = '*****'

client = MongoClient(username=user, password=pwd)

db = client.veggieDB

raws = db.posts
vegans = db.veg_posts
vegetarians = db.veggie_posts

raw_posts = raws.find({},{'_id':0})
vegan_posts = vegans.find({},{'_id':0})
vegetarian_posts = vegetarians.find({},{'_id':0})

p1 = list(raw_posts)
p2 = list(vegan_posts)
p3 = list(vegetarian_posts)

posts = p1 + p2 + p3

s = json.dumps(posts)

f = open('posts.txt', 'w')
f.write(s)
f.close()

