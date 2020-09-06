# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class _BaseItem(Item):
    id = Field()
    crawl_time = Field()
    update_time = Field()
    spider_name = Field()


class ArticleItem(_BaseItem):
    title = Field()
    url = Field()
    position = Field()
    mall = Field()
    img = Field()


class CommentItem(_BaseItem):
    article_id = Field()
    goods_type = Field()
    user_name = Field()
    user_id = Field()
    user_url = Field()
    position = Field()
    pub_time = Field()
    come_from = Field()
    comment_id = Field()
    comment_info = Field()
    comment_quote_id = Field()
