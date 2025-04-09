import scrapy
from urllib.parse import urljoin
import redis
import trafilatura
# from ..items import NewSpiderItem
import re


class NewSpider(scrapy.Spider):
    name = "newspider"
    allowed_domains = ["example.com"]  # 请替换为实际域名
    start_urls = ["https://www.example.com"]  # 请替换为实际起始 URL

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Referer": "https://www.example.com",  # 请替换为实际 Referer
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0"
        }
        self.redis_host = None
        self.redis_port = None
        self.redis_db = None
        self.redis_url_key = None
        self.redis_client = None

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        spider.redis_host = spider.settings.get('REDIS_HOST', 'localhost')
        spider.redis_port = spider.settings.getint('REDIS_PORT', 6379)
        spider.redis_db = spider.settings.getint('REDIS_DB', 0)
        spider.redis_url_key = spider.settings.get('REDIS_URL_KEY', 'newspider:url')
        spider.redis_client = redis.StrictRedis(
            host=spider.redis_host,
            port=spider.redis_port,
            db=spider.redis_db
        )
        return spider

    def start_requests(self):
        """初始请求"""
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                headers=self.headers,
                meta={'dont_merge_cookies': True}
            )

    def parse(self, response):
        """解析列表页，提取文章链接"""
        self.logger.info(f"Parsing list page: {response.url}")
        # 请根据实际情况修改 CSS 选择器
        links = response.css('a.article-link::attr(href)').getall()
        self.logger.info(f"Found {len(links)} articles on the page")

        for relative_url in links:
            full_url = urljoin(response.url, relative_url)
            if not self.redis_client.sismember(self.redis_url_key, full_url):
                self.redis_client.sadd(self.redis_url_key, full_url)
                self.logger.info(f"New URL found: {full_url}")
                yield response.follow(
                    full_url,
                    callback=self.parse_article,
                    headers=self.headers,
                    meta={'dont_merge_cookies': True}
                )

    def parse_article(self, response):
        """解析文章页，生成 Item"""
        item = NewSpiderItem()
        item['url'] = response.url
        item['author'] = 'Unknown'  # 可根据实际情况修改
        item['time'] = 'Unknown'  # 可根据实际情况修改

        # 使用 Trafilatura 提取文章内容
        extracted_text = trafilatura.extract(response.text)
        item['article_content'] = extracted_text if extracted_text else ""

        # 直接截取前 200 个字符作为标题
        if extracted_text:
            item['title'] = extracted_text[:200].strip()
        else:
            item['title'] = "未找到主题信息"

        yield item
