# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Item
from twisted.enterprise import adbapi
from pymongo import MongoClient
import redis


class BookPipeline(object):
    review_rating_map = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    def process_item(self, item, spider):
        rating = item.get('review_rating')
        if rating:
            item['review_rating'] = self.review_rating_map[rating]
        return item


# mysql> create database scrapy_db;
# mysql> use scrapy_db;
# mysql> create table books(
# -> upc char(16) not null primary key,
# -> name varchar(256) not null,
# -> price varchar(16) not null,
# -> review_rating int,
# -> review_num int,
# -> stock int
# -> );
class MySQLPipeline:
    def open_spider(self, spider):
        db = spider.setting.get('MYSQL_DB_NAME', 'scrapy_default')
        host = spider.setting.get('MYSQL_HOST', 'localhost')
        port = spider.setting.get('MYSQL_PORT', 3306)
        user = spider.setting.get('MYSQL_USER', 'root')
        passwd = spider.setting.get('MYSQL_PASSWORD', '123...')

        self.dbpool = adbapi.ConnectionPool('MySQLdb', host=host, port=port, db=db, user=user, passwd=passwd, charset='utf8')

    def close_spider(self, spider):
        self.dbpool.close()

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.insert_db, item)
        return item

    def insert_db(self, tx, item):
        values = (
            item['upc'],
            item['name'],
            item['price'],
            item['review_rating'],
            item['review_num'],
            item['stock'],
        )

        sql = 'INSERT INTO books VALUES (%s, %s, %s, %s, %s, %s)'
        tx.execute(sql, values)


class MongoDBPipeline:
    def open_spider(self, spider):
        db_uri = spider.setting.get('MONGODB_URI', 'mongodb://localhost:27017')
        db_name = spider.setting.get('MONGODB_DB_NAME', 'scrapy_default')

        self.db_client = MongoClient('mongodb://localhost:27017')
        self.db = self.db_client[db_name]

    def close_spider(self, spider):
        self.db_client.close()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):
        if isinstance(item, Item):
            item = dict(item)
        self.db.books.insert_one(item)


class RedisPipeline:
    def open_spider(self, spider):
        db_host = spider.setting.get('REDIS_HOST', 'localhost')
        db_port = spider.setting.get('REDIS_PORT', 6379)
        db_index = spider.setting.get('REDIS_DB_INDEX', 0)

        self.db_conn = redis.StrictRedis(host=db_host, port=db_port, db=db_index)
        self.item_i = 0

    def close_spider(self, spider):
        self.db_conn.connection_pool.disconnect()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):
        if isinstance(item, Item):
            item = dict(item)
        self.item_i += 1
        self.db_conn.hmset('book:%s' % self.item_i, item)