import scrapy
import re
from maoyan_movies.items import MaoyanMoviesItem
from scrapy.selector import Selector
from fake_useragent import UserAgent

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']


    def __init__(self):
        ua = UserAgent(verify_ssl=False)
        cookies ='uuid_n_v=v1; uuid=37ADCBB0B82C11EA85DD839D6F814C7A07C97AE801FF4DC8BD8250A845B873E6; _csrf=32877a02a8d04b39e3f222e6b4252e292c0973a18db32cd60d8b7d80615581a7; _lxsdk_cuid=172f3f8be8ac8-08fdf560b8b4c8-4b5469-13c680-172f3f8be8ac8; _lxsdk=37ADCBB0B82C11EA85DD839D6F814C7A07C97AE801FF4DC8BD8250A845B873E6; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593911782,1593950967,1593951682,1593953019; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593953946; __mta=210704298.1593231064909.1593321142354.1593953946484.8; mojo-uuid=3533b1aaa282adefb81243b93761bc8c; _lxsdk_s=1731ee14f08-ce7-afe-843%7C%7C24; mojo-trace-id=15; mojo-session-id={"id":"52c5fbd84ad14a38b3e9c7a3abc42660","time":1593950949210}'
        self.header = {'cookies':str(cookies),'user-agent':ua.random}

    def start_requests(self):

        url='http://maoyan.com/films?showType=3'
        try:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.header, dont_filter=False)
        except Exception as e:
            print(e)

    def parse(self, response):
        movies = Selector(response=response).xpath('//div[@class="channel-detail movie-item-title"]')
        try:
            for movie in movies[0:10]:
                item = MaoyanMoviesItem()
                link_uri = movie.xpath('./a/@href').extract_first().strip()
                link = 'https://maoyan.com' + link_uri
                item['link'] = link
                yield scrapy.Request(url=link, meta={'item': item}, callback=self.parse2)
        except Exception as e:
            print(e)

    def parse2(self, response):
        try:
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
        except Exception as e:
            print(e)