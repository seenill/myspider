import scrapy
import json
import urllib.parse
from urllib.parse import urlencode

class BestblogsSpider(scrapy.Spider):
    name = 'bestblogs_spider'
    allowed_domains = ['bestblogs.dev']
    start_urls = ['https://www.bestblogs.dev/feeds?category=programming']

    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 3,
        'DEFAULT_REQUEST_HEADERS': {
            'Host': 'www.bestblogs.dev',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'cookie': 'NEXT_LOCALE=zh'
        }
    }

    def parse(self, response):
        print(response.text)
        # 解析文章列表
        articles = response.css('div.feed-item')
        for article in articles:
            yield {
                'title': article.css('h2.title::text').get(),
                'url': response.urljoin(article.css('a::attr(href)').get()),
                'author': article.css('div.author::text').get(),
                'publish_date': article.css('div.date::text').get(),
                'category': 'programming'
            }

        # 处理分页
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)