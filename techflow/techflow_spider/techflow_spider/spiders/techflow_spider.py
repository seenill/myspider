import scrapy
from urllib.parse import urljoin
import redis
import trafilatura
from ..items import TechflowItem
import re


class TechflowSpider(scrapy.Spider):
    name = "techflow"
    allowed_domains = ["techflowpost.com"]
    start_urls = ["https://www.techflowpost.com/article/index.html"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = {
            "authority": "www.techflowpost.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "max-age=0",
            "cookie": "ASP.NET_SessionId=k1hiq2z1x50fd3jbjyppecfi; zh_choose=s",
            "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
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
        spider.redis_url_key = spider.settings.get('REDIS_URL_KEY', 'techflow:url')
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
        item = TechflowItem()
        item['url'] = response.url
        """解析列表页，提取文章链接"""
        self.logger.info(f"Parsing list page: {response.url}")
        links = response.css('a.tit.row1.fw.dfont::attr(href)').getall()
        self.logger.info(f"Found {len(links)} articles on the page")

        for relative_url in links:
            full_url = urljoin("https://www.techflowpost.com", relative_url)
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
        item = TechflowItem()
        item['url'] = response.url
        item['author'] = 'TechFlow深渊'
        item['time'] = response.css('div.time.font-i.fw::text').get()
        # 使用 Trafilatura 提取文章内容
        extracted_text = trafilatura.extract(response.text)
        item['article_content'] = extracted_text if extracted_text else ""

        # 查找第一个中文字符的位置
        first_chinese_index = next((i for i, char in enumerate(extracted_text) if re.match(r'[\u4e00-\u9fff]', char)), None)
        if first_chinese_index is not None:
            item['title'] = extracted_text[first_chinese_index:first_chinese_index + 200].strip()
        else:
            item['title'] = "未找到主题信息"

        print(item)
        yield item