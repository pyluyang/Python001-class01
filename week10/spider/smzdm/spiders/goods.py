# -*- coding: utf-8 -*-

import ast
import datetime
import re

import scrapy
from crawl_utils.scrapy.core import ErrorCallback

from ..items import ArticleItem, CommentItem


class GoodsSpider(scrapy.Spider, ErrorCallback):
    name = 'goods'
    allowed_domains = ['smzdm.com']

    def __init__(self, category, limit=30):
        # i.e. qipaoshui
        self.category = category
        self.count = 0
        self.limit = int(limit)
        self.position_dict = {
            "沙发": "1楼",
            "椅子": "2楼",
            "板凳": "3楼",
        }
        self._datetime = datetime.datetime
        self._timedelta = datetime.timedelta
        self.minutes_ago_pattern = re.compile(r"(\d+)分钟前")
        self.hours_ago_pattern = re.compile(r"(\d+)小时前")
        self.img_emotion_pattern = re.compile(r"""<img[^>]*alt="([^"]+)"[^>]*>""")
        self.img_mosaic_pattern = re.compile(r"""<img[^>]*mosaic[^>]*>""")
        self.MOSAIC = "[MOSAIC]"
        self.tag_pattern = re.compile(r"<[^>]*>")
        self.emotion_space_pattern = re.compile(r"(?<=])\ +(?=\[)")

    def start_requests(self):
        url = f"https://www.smzdm.com/fenlei/{self.category}/"
        yield scrapy.Request(url, meta={'count': 0}, errback=self.errback)

    def parse(self, response):
        count = response.meta['count']
        for div in response.css("#feed-main-list li > div"):
            count += 1
            if count > self.limit:
                break
            title_tag = div.css("h5 a")
            article_url = title_tag.xpath("@href").get()
            article_id = title_tag.xpath("@href").re_first(r"/p/(\d+)")
            article_data = title_tag.xpath("@onclick").re_first(r"push\((.*)\)")
            article_data = ast.literal_eval(article_data)
            position = article_data['position']
            article_title = article_data['pagetitle']
            mall = article_data['商城']
            img = div.css(".z-feed-img a img::attr(src)").get()
            img = response.urljoin(img)

            yield ArticleItem(**{
                'id': article_id,
                'title': article_title,
                'url': article_url,
                'position': position,
                'mall': mall,
                'img': img,
            })
            yield scrapy.Request(article_url, callback=self.parse_comments, meta={'article_id': article_id},
                                 errback=self.errback)

        next_url = response.css(".feed-pagenation .next-page a::attr(href)").get()
        if count <= self.limit and next_url:
            yield scrapy.Request(next_url, meta={'count': count}, errback=self.errback)

    def parse_comments(self, response):
        article_id = response.meta['article_id']
        goods_type = response.css("div.crumbs a > span::text").getall()[-1]
        for li in response.css("#commentTabBlockNew li.comment_list"):
            user_info = self._parse_user_info(li.css(".comment_avatar_time > a.user_name"))
            position = li.css(".comment_avatar span.grey::text").get()
            position = self.position_dict.get(position, position)
            pub_time = self._parse_time(li)
            come_from = li.css("span.come_from a::text").get()
            comment_tag = li.css(".comment_conBox > .comment_conWrap .comment_con")
            comment_id = comment_tag.css("input::attr(comment-id)").get()
            comment_info = self._parse_comments(comment_tag.css("p").get())
            # More comments quote, i.e: https://www.smzdm.com/p/8908644/
            # 回复别人的评论时, 有可能有多条, 超过3条页面上会隐藏,而获取所有的记录需要发请求
            # 因此这里不记录每条评论下所有引用的评论(如果有的话),而是记录最后一条引用的评论
            # 若需要还原为完整的回复链, 根据该字段递归查找
            comment_quote_id = li.css(
                ".comment_conBox > .blockquote_wrap > blockquote:last-child::attr(blockquote_cid)").get()
            yield CommentItem(**{
                'id': f"{article_id}_{comment_id}",
                'article_id': article_id,
                **user_info,
                'goods_type': goods_type,
                'position': position,
                'pub_time': pub_time,
                'come_from': come_from,
                'comment_id': comment_id,
                'comment_info': comment_info,
                'comment_quote_id': comment_quote_id,
            })

        # i.e. https://www.smzdm.com/p/23523045/
        next_url = response.css("#commentTabBlockNew .pagination .pagedown a::attr(href)").get()
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse_comments, meta={'article_id': article_id},
                                 errback=self.errback)

    def _parse_user_info(self, tag):
        return {
            'user_name': tag.css("span::text").get(),
            'user_id': tag.xpath("@usmzdmid").get(),
            'user_url': tag.xpath("@href").get(),
        }

    def _parse_comments(self, html):
        """保留表情顺序
        样例: https://regex101.com/r/CrHF9B/1  (v1/v2/v3)
        """
        if not html:
            return html
        if self.img_emotion_pattern.search(html):
            html = self.img_emotion_pattern.sub("\g<1>", html)
        if self.img_mosaic_pattern.search(html):
            # i.e. https://www.smzdm.com/p/23645559/
            html = self.img_mosaic_pattern.sub(self.MOSAIC, html)
        html = self.tag_pattern.sub("", html)
        html = self.emotion_space_pattern.sub("", html)
        if html:
            html = html.strip()
        return html

    def _parse_time(self, sel):
        def _outtime(ptime):
            return ptime.strftime("%Y-%m-%d %H:%M")

        pub_time1 = sel.css(".time meta::attr(content)").get()
        pub_time2 = sel.css(".time::text").get()
        pub_time = self._datetime.strptime(pub_time1, "%Y-%m-%d")

        try:
            # https://www.smzdm.com/p/23523045/p3/#comments
            tmp = self._datetime.strptime(pub_time2, "%m-%d %H:%M")
            pub_time = pub_time.replace(month=tmp.month, day=tmp.day, hour=tmp.hour, minute=tmp.minute)
            return _outtime(pub_time)
        except ValueError:
            if pub_time2 == pub_time1 or not pub_time2:
                # https://www.smzdm.com/p/8908644
                return _outtime(pub_time)
            elif self.hours_ago_pattern.search(pub_time2):
                hour = int(self.hours_ago_pattern.search(pub_time2).group(1))
                pub_time = self._datetime.now() - self._timedelta(seconds=hour * 3600)
                return _outtime(pub_time)
            elif self.minutes_ago_pattern.search(pub_time2):
                minutes = int(self.minutes_ago_pattern.search(pub_time2).group(1))
                pub_time = self._datetime.now() - self._timedelta(seconds=minutes * 60)
                return _outtime(pub_time)
        return _outtime(pub_time)
