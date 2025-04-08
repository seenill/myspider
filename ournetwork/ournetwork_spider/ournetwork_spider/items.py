# items.py
import scrapy

class OurNetworkItem(scrapy.Item):
    url = scrapy.Field()
    publish_time = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    author = scrapy.Field()