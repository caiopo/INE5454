import scrapy


class NewsItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
    location = scrapy.Field()
    diseases = scrapy.Field()

    retrieved_datetime = scrapy.Field()
    depth = scrapy.Field()
