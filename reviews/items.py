# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    reviews = scrapy.Field()
    retrieved_datetime = scrapy.Field()


class Review(scrapy.Item):
    rating = scrapy.Field()
    comment = scrapy.Field()
    date = scrapy.Field()
