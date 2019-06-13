# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class ZhihuuserPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):
    collection_name = 'users'

    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db = self.client['mydb']
        self.colle = self.db['知乎']

    def process_item(self, item, spider):
        self.colle.update({'url_token':item['url_token']},dict(item),True)
        return item