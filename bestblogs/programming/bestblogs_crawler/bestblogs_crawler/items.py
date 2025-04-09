import scrapy

class BestblogsItem(scrapy.Item):
    # 已有的字段
    url = scrapy.Field()
    author = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    article_content = scrapy.Field()