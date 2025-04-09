import logging
import re
import scrapy
from urllib.parse import urljoin
import trafilatura
import redis
from ..items import OurNetworkItem  # 替换为实际项目名


class OurNetworkSpider(scrapy.Spider):
    name = "ournetwork"
    allowed_domains = ["ournetwork.xyz"]
    start_urls = ["https://www.ournetwork.xyz/"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        spider.redis_url_key = spider.settings.get('REDIS_URL_KEY', 'ournetwork-urls')
        spider.redis_client = redis.StrictRedis(
            host=spider.redis_host,
            port=spider.redis_port,
            db=spider.redis_db
        )
        try:
            spider.redis_client = redis.StrictRedis(
                host=spider.redis_host,
                port=spider.redis_port,
                db=spider.redis_db
            )
            # 测试 Redis 连接
            spider.redis_client.ping()
            logging.info("Redis 连接成功")
        except redis.ConnectionError:
            logging.error("无法连接到 Redis 服务器")
        return spider


    def parse(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': 'https://www.ournetwork.xyz/',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
        }

        links = response.css('a[href^="/p/"]::attr(href)').getall()[:5]
        base_url = 'https://www.ournetwork.xyz'
        for href in links:
            full_url = urljoin(base_url, href)
            if not self.redis_client.sismember(self.redis_url_key, full_url):
                self.redis_client.sadd(self.redis_url_key, full_url)
                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse_article,
                    meta={'url': full_url},
                    headers=headers
                )

    def parse_article(self, response):
        print(response.url)
        """解析文章页，生成 Item"""
        item = OurNetworkItem()
        try:
            item["author"] = "ournetwork"
            item['url'] = response.meta['url']
            item['time'] = response.css('header.gh-article-header p.text-xs::text').get().strip()

            # 使用 Trafilatura 提取文章内容
            extracted_text = trafilatura.extract(response.text)
            item['article_content'] = extracted_text if extracted_text else ""

            # 查找图片元素
            img_index = response.text.find('<img')
            if img_index != -1:
                # 从图片位置之后开始截取
                text_after_img = extracted_text[img_index:]
            else:
                text_after_img = extracted_text

            # 截取前200个字符
            if len(text_after_img) > 200:
                item['title'] = text_after_img[:200].strip() + '...'
            else:
                item['title'] = text_after_img.strip()

            # 如果截取后标题为空，再次尝试从原始提取内容截取
            if not item['title']:
                if len(extracted_text) > 200:
                    item['title'] = extracted_text[:200].strip() + '...'
                else:
                    item['title'] = extracted_text.strip()

            # 如果最终标题仍为空，设置默认标题
            if not item['title']:
                item['title'] = '未找到标题信息'
        except Exception as e:
            self.logger.error(f"解析失败: {e}")
            item['time'] = '解析失败'
            item['title'] = '解析失败'
            item['article_content'] = ''
        yield item