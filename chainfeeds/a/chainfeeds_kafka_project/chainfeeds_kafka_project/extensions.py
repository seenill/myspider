import time
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


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
        # 修改这里，去掉 spider 参数
        if self.crawler.engine.spider_is_idle():
            return

        time.sleep(self.interval)
        process = CrawlerProcess(get_project_settings())
        process.crawl('chainfeeds')
        process.start()