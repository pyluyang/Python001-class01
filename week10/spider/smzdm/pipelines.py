# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time

import mysql.connector

from .items import ArticleItem, CommentItem


class BasePipeline:
    def process_item(self, item, spider):
        crawl_time = time.strftime("%Y-%m-%d %H:%M:%S")
        item.update({
            'spider_name': spider.name,
            'crawl_time': crawl_time,
            'update_time': crawl_time,
        })
        return item


class MysqlPipelineBase:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            port=crawler.settings.get('MYSQL_PORT'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            database=crawler.settings.get('MYSQL_DATABASE'),
        )

    def open_spider(self, spider):
        self.cnx = mysql.connector.connect(
            host=self.host, port=self.port,
            user=self.user, password=self.password,
            database=self.database,
        )
        self.cursor = self.cnx.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.cnx.close()

    def process_item(self, item, spider):
        raise NotImplemented


class MysqlPipeline(MysqlPipelineBase):
    def process_item(self, item, spider):
        if type(item) == ArticleItem:
            table = 'article'
        elif type(item) == CommentItem:
            table = 'comment'
        keys = ', '.join(item.keys())
        values = ', '.join([f'%({i})s' for i in item])
        add_item = ("INSERT INTO %s (%s) VALUES (%s)" % (table, keys, values))
        try:
            self.cursor.execute(add_item, dict(item))
            self.cnx.commit()
        except Exception as e:
            spider.logger.error(e)
            self.cnx.rollback()
        return item
