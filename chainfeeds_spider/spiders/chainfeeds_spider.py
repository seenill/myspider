# 文件名: chainfeeds_spider.py
import requests
import scrapy
import json
import time
from urllib.parse import urljoin
from scrapy import signals
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class SubstackItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    publish_time = scrapy.Field()
    author = scrapy.Field()


class ChainfeedsSpider(scrapy.Spider):
    name = "chainfeeds"
    allowed_domains = ["substack.chainfeeds.xyz"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_url = None  # 用于存储上一次的 URL
        self.start_url = kwargs.get('start_url', 'https://substack.chainfeeds.xyz/s/daily')

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_url,
            cookies=self.settings.getdict('SITE_COOKIES'),
            callback=self.parse,
            meta={'dont_merge_cookies': True}
        )

    def parse(self, response):
        if "ChainFeeds Newsletter" not in response.text:
            self.logger.error("Cookie登录验证失败")
            return

        articles = response.css('div.post-preview')
        for article in articles[:5]:  # 取最新5篇文章
            time_str = article.css('time::attr(datetime)').get()
            relative_url = article.css('a.post-preview-title::attr(href)').get()

            if relative_url:
                yield response.follow(
                    url=relative_url,
                    callback=self.parse_article,
                    meta={'publish_time': time_str}
                )

    def parse_article(self, response):
        """解析文章详情页"""
        current_url = response.url

        # 检查是否为新内容
        if self.last_url and current_url == self.last_url:
            self.logger.info("检测到重复URL: %s", current_url)
            return

        self.last_url = current_url

        item = SubstackItem()
        item['url'] = current_url
        item['publish_time'] = response.meta['publish_time']
        item['title'] = response.css('h1.post-title::text').get()
        item['author'] = response.css('div.post-author::text').get()
        item['content'] = '\n'.join(response.css('div.post-content p::text').getall())

        yield item


class FeishuPipeline:
    """飞书消息推送管道"""

    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            webhook_url=crawler.settings.get('FEISHU_WEBHOOK')
        )

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        message = {
            "msg_type": "text",
            "content": {
                "text": f"新文章通知\n标题：{adapter['title']}\n作者：{adapter['author']}\n链接：{adapter['url']}"
            }
        }

        try:
            response = requests.post(
                self.webhook_url,
                data=json.dumps(message),
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            spider.logger.info(f"飞书消息发送成功: {adapter['url']}")
        except Exception as e:
            spider.logger.error(f"飞书消息发送失败: {str(e)}")

        return item


class SchedulerExtension:
    """定时调度扩展"""

    def __init__(self, crawler):
        self.crawler = crawler
        self.interval = crawler.settings.getint('SCHEDULE_INTERVAL', 300)

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext

    def spider_closed(self, spider, reason):
        """爬虫关闭时调度下次任务"""
        if self.crawler.engine.spider_is_open(spider):
            return

        time.sleep(self.interval)
        process = CrawlerProcess(get_project_settings())
        process.crawl(ChainfeedsSpider)
        process.start()


if __name__ == "__main__":
    settings = get_project_settings()
    settings.update({
        'ITEM_PIPELINES': {
            'chainfeeds_spider.FeishuPipeline': 300,
        },
        'FEISHU_WEBHOOK': 'https://open.feishu.cn/...你的webhook地址...',
        'SITE_COOKIES': {
            # 从settings.py加载或使用环境变量
            'connect.sid': 's%3AvNcZtQppA9w2lauu9AMC0eqyNLDfOVfL...'
        },
        'SCHEDULE_INTERVAL': 300  # 5分钟
    })

    process = CrawlerProcess(settings)
    process.crawl(ChainfeedsSpider)
    process.start()