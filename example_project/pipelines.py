# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import psycopg2

TABLE = 'client_posts'


class PostsPipeline(object):
    def __init__(self):
        self.hostname = 'localhost'
        self.username = 'postgres'
        self.password = '1q2w3e' # your password
        self.database = 'ycombinator'
        self.connection = None
        self.cursor = None

    def open_spider(self, spider):
        self.connection = psycopg2.connect(
            host=self.hostname,
            user=self.username,
            password=self.password,
            dbname=self.database
        )
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute(
            f"INSERT INTO {TABLE}(url,title,created) VALUES('{item['url'][0]}', '{item['title'][0]}', now())"
        )
        self.connection.commit()
        return item
