import scrapy
import re
from maoyan_movies.items import MaoyanMoviesItem
from scrapy.selector import Selector

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def parse(self, response):
        movies = Selector(response=response).xpath('//div[@class="channel-detail movie-item-title"]')
        for movie in movies[0:10]:
            item = MaoyanMoviesItem()
            link_uri = movie.xpath('./a/@href').extract_first().strip()
            link = 'https://maoyan.com' + link_uri
            item['link'] = link
            yield scrapy.Request(url=link, meta={'item': item}, callback=self.parse2)


    def parse2(self, response):
        movie = Selector(response=response).xpath('//div[@class="movie-brief-container"]')
        item = response.meta['item']
        film_name = movie.xpath('./h1/text()').extract_first().strip()
        item['film_name'] = film_name
        
        film_types = movie.xpath('./ul/li[1]/*/text()').extract()
        item['film_types'] = ','.join(film_types)

        release_date = movie.xpath('./ul/li[3]/text()').extract_first().strip()
        release_date_update = re.sub(r'[^\d-]', "", release_date)
        item['plan_date'] = release_date_update
        
        yield item