import random
from scrapy import signals
# from fake_useragent import UserAgent

class RandomUserAgentMiddleware:
    # def __init__(self):
    #     self.ua = UserAgent()

    def process_request(self, request, spider):
        request.headers['User-Agent'] = self.ua.random

class ProxyMiddleware:
    def __init__(self, proxy_list):
        self.proxies = proxy_list

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('PROXIES'))

    def process_request(self, request, spider):
        request.meta['proxy'] = random.choice(self.proxies)