import scrapy
from urllib.parse import urljoin
from ..items import BlockbeatsSpiderItem
import re
import redis
import trafilatura  # 导入 trafilatura 库

class BlockbeatsSpider(scrapy.Spider):
    name = "blockbeats"
    allowed_domains = ["theblockbeats.info"]
    start_urls = ["https://www.theblockbeats.info/article"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = {
            "Host": "www.theblockbeats.info",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9",
            "cookie": "lang=cn; _ga=GA1.1.544756758.1743643931; theme=dark; farcaster_id=0; _ga_98K0QJM9BB=GS1.1.1743679954.3.1.1743682184.0",
            "if-none-match": '"135d1-uS9O+1q2V/ckn/T3HVuI6U3mhvk"',
            "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }
        self.time_pattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')
        self.redis_host = None
        self.redis_port = None
        self.redis_db = None
        self.redis_url_key = None
        self.redis_client = None

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        spider.redis_host = crawler.settings.get('REDIS_HOST', 'localhost')
        spider.redis_port = crawler.settings.getint('REDIS_PORT', 6379)
        spider.redis_db = crawler.settings.getint('REDIS_DB', 0)
        spider.redis_url_key = crawler.settings.get('REDIS_URL_KEY', 'blockbeats-url')
        spider.redis_client = redis.StrictRedis(
            host=spider.redis_host,
            port=spider.redis_port,
            db=spider.redis_db
        )
        return spider

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            headers=self.headers,
            meta={'dont_merge_cookies': True}
        )

    def parse(self, response):
        # 提取文章链接
        article_links = response.css('a.article-item-title.title-item::attr(href)').getall()

        # 拼接完整URL并生成请求
        for href in article_links[:5]:
            full_url = urljoin(response.url, href)
            if not self.redis_client.sismember(self.redis_url_key, full_url):
                self.redis_client.sadd(self.redis_url_key, full_url)
                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse_article,
                    headers=self.headers,
                    meta={'dont_merge_cookies': True}
                )

    def parse_article(self, response):
        try:
            item = BlockbeatsSpiderItem()

            # 使用 Trafilatura 提取文章内容
            extracted_text = trafilatura.extract(response.text)  # 调用 trafilatura.extract 方法提取内容
            item['article_content'] = extracted_text

            # 提取标题，直接取前200个字
            item['title'] = extracted_text[:200].strip() if extracted_text else "未找到主题信息"

            # 提取时间
            item['time'] = None
            for span in response.css('span'):
                time_text = span.get().strip()
                if self.time_pattern.search(time_text) and '分钟' not in time_text:
                    item['time'] = self.time_pattern.search(time_text).group()
                    break

            # 提取URL和作者
            item['url'] = response.url
            item['author'] = '区块律动-BlockBeats'

            yield item

        except Exception as e:
            self.logger.error(f"处理文章页面 {response.url} 时发生错误: {e}")