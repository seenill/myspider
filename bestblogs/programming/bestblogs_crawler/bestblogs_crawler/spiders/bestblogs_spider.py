import scrapy
from urllib.parse import urljoin
import redis
import trafilatura
import json
import re


class BestblogsSpider(scrapy.Spider):
    name = "bestblogs_spider"
    allowed_domains = ["bestblogs.dev"]  # 请替换为实际域名
    start_urls = ["https://api.bestblogs.dev/api/resource/list"]  # 请替换为实际起始 URL

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://www.bestblogs.dev',
            'Referer': 'https://www.bestblogs.dev/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'User-Id': 'VU_1ae5fc',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
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
        spider.redis_url_key = spider.settings.get('REDIS_URL_KEY', 'bestblogs-url')
        spider.redis_client = redis.StrictRedis(
            host=spider.redis_host,
            port=spider.redis_port,
            db=spider.redis_db
        )
        return spider

    def start_requests(self):
        """初始请求"""
        json_data = {
            'keyword': '',
            'qualifiedFilter': '',
            'sourceId': '',
            'collectionId': '',
            'category': 'programming',  # 仅保留分类名称
            'timeFilter': '1w',         # 时间范围（1周内）
            'language': 'all',          # 语言类型
            'userLanguage': 'zh',       # 用户语言
            'sortType': 'time_desc',    # 关键参数：按时间降序排序
            'currentPage': 1,
            'pageSize': 10,
        }

        yield scrapy.Request(
            url=self.start_urls[0],
            method='POST',
            headers=self.headers,
            body=json.dumps(json_data),
            callback=self.parse,
            meta={'dont_merge_cookies': True}
        )

    def parse(self, response):
        """解析响应，提取文章链接"""
        self.logger.info(f"Parsing response: {response.url}")
        try:
            data = json.loads(response.text)
            data_list = data.get('data', {}).get('dataList', [])
            for item in data_list:
                article_url = item.get('url')
                print(article_url)
                if article_url:
                    # 检查 URL 是否符合预期格式（可选，根据实际情况调整）
                    if isinstance(article_url, str) and article_url.startswith(('http://', 'https://')):
                        if not self.redis_client.sismember(self.redis_url_key, article_url):
                            self.redis_client.sadd(self.redis_url_key, article_url)
                            self.logger.info(f"New URL found: {article_url}")
                            yield response.follow(
                                article_url,
                                callback=self.parse_article,
                                headers=self.headers,
                                meta={'dont_merge_cookies': True}
                            )
                    else:
                        self.logger.warning(f"Invalid URL format: {article_url}")
                else:
                    self.logger.warning(f"URL not found in item: {item}")  # 记录没有找到 URL 的情况
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON Decode Error: {e}")
        except Exception as ex:
            self.logger.error(f"An unexpected error occurred: {ex}")  # 捕获其他异常并记录

    def parse_article(self, response):
        print(response.url)
        """解析文章页，生成 Item"""
        item = {}  # 这里先简单使用字典，你可以根据需要定义 Item 类
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
        print(item)
        yield item