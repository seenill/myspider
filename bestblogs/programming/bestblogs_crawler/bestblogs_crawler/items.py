import scrapy

class BestblogsItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    publish_time = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field()
    score = scrapy.Field()