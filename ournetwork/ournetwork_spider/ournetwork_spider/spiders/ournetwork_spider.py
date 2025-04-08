import scrapy
from urllib.parse import urljoin
from ..items import OurNetworkItem  # 替换为实际项目名

class OurNetworkSpider(scrapy.Spider):
    name = "ournetwork"
    allowed_domains = ["ournetwork.xyz"]
    start_urls = ["https://www.ournetwork.xyz/"]

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
            yield scrapy.Request(
                url=full_url,
                callback=self.parse_article,
                meta={'url': full_url},
                headers=headers
            )

    def parse_article(self, response):
        item = OurNetworkItem()
        try:
            item["author"]= "ournetwork"
            item['url'] = response.meta['url']
            item['publish_time'] = response.css('header.gh-article-header p.text-xs::text').get().strip()
            item['title'] = response.css('header.gh-article-header h1::text').get().strip()
            item['subtitle'] = response.css('header.gh-article-header div.text-xl::text').get().strip()
            print(item)
        except Exception as e:
            self.logger.error(f"解析失败: {e}")
            item['publish_time'] = '解析失败'
            item['title'] = '解析失败'
            item['subtitle'] = '解析失败'
        yield item