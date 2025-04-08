import scrapy


class SubstackItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    time = scrapy.Field()
    author = scrapy.Field()