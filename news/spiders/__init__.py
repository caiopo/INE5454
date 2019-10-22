from datetime import datetime

import scrapy

from news.extractors import extract_title, extract_content, extract_diseases, extract_location
from news.items import NewsItem


class NewsSpider(scrapy.Spider):
    name = 'newsbot'

    start_urls = [
        'https://g1.globo.com/sp/santos-regiao/noticia/2019/10/11/'
        'macaco-morto-com-suspeita-de-febre-amarela-e-encontrado-em-eldorado-sp.ghtml',
    ]

    def parse(self, response):
        content = extract_content(response)

        yield NewsItem(
            title=extract_title(response),
            diseases=extract_diseases(content),
            location=extract_location(content),
            retrieved_datetime=datetime.now(),
            url=response.request.url,
            content=content,
        )

        yield from self.get_links(response)

    def get_links(self, response):
        for a in response.xpath('//body//a/@href'):
            url = a.get()
            yield response.follow(url, self.parse)
