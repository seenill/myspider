import scrapy
from urllib.parse import urljoin
import re


class BlockbeatsSpiderItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    author = scrapy.Field()


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
            yield scrapy.Request(
                url=full_url,
                callback=self.parse_article,
                headers=self.headers,
                meta={'dont_merge_cookies': True}
            )

    def parse_article(self, response):
        try:
            item = BlockbeatsSpiderItem()

            # 提取标题
            item['title'] = response.css('h1::text').get().strip() if response.css('h1::text').get() else None

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