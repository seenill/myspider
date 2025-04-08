import scrapy
from urllib.parse import urljoin


class ChainfeedsSpider(scrapy.Spider):

    name = "chainfeeds"
    allowed_domains = ["substack.chainfeeds.xyz"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_url = None  # 用于存储上一次的 URL
        self.start_url = kwargs.get('start_url', 'https://substack.chainfeeds.xyz/s/pro')

    def start_requests(self):
        headers = {
            "authority": "substack.chainfeeds.xyz",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "max-age=0",
            "cookie": "ab_experiment_sampled=%22false%22; ab_testing_id=%220449f7d4-6942-4423-b654-25ba102c263d%22; ajs_anonymous_id=%22d5a13b83-6cca-46e4-8a5f-b5e4ca3ecab4%22; cookie_storage_key=556f216f-0492-49c4-9067-354c338a4d8f; _gcl_au=1.1.1297430761.1742978752; intro_popup_last_hidden_at=2025-03-26T09:11:50.743Z; connect.sid=s%3An31pDuw9MZrBACcZhLx7XqcSs6qhjqS5.hLXJdjN7VxHutBDNkexrynSUtFwQEnc%2FvUHVCGJSPsA; ajs_anonymous_id=%228eea04c2-deb8-466a-b555-05de8ea34307%22; visit_id=%7B%22id%22%3A%2250187c27-5f30-4f85-87a3-cc4dd39ef87c%22%2C%22timestamp%22%3A%222025-04-02T16%3A24%3A43.839Z%22%7D; __cf_bm=9ZQ0DYM9wxyNBhNq9kcF1KlF.r59nZILIqjm6W4YQA8-1743613071-1.0.1.1-lI1eBe__J3_XKDi6bYIsgWiOJPQ3frAukqrZ6SfZkQzdkFnyHsfTEuA..q6svI0LFWTI8.BshIEn1W7Mfd4pBVF0z05UtnJiVxgsNl1pZ3Q; AWSALBTG=4ToJ6DasQPJ1kKjX4BYpeBggSaI6sCDLc50Qoa48vvzJNVjnJE4TAUlRlmIf0iywu9huQlfZYMXd6yihGW4aVcc8dku39HMvzEGwxF4mcka1wMZ1j3SFttMtR0entUKoGU2rDMG8YECSGLfbAwQf0/0dWjTGBPhLA4o2sQhmjvNK; AWSALBTGCORS=4ToJ6DasQPJ1kKjX4BYpeBggSaI6sCDLc50Qoa48vvzJNVjnJE4TAUlRlmIf0iywu9huQlfZYMXd6yihGW4aVcc8dku39HMvzEGwxF4mcka1wMZ1j3SFttMtR0entUKoGU2rDMG8YECSGLfbAwQf0/0dWjTGBPhLA4o2sQhmjvNK; _dd_s=rum=0&expire=1743614131714",
            "if-none-match": 'W/"41-JUlMLVVaXzVvwvkqWvy0XD2aODQ"',
            "priority": "u=0, i",
            "referer": "https://substack.chainfeeds.xyz/p/prozktls",
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

        yield scrapy.Request(
            url=self.start_url,
            # cookies=self.settings.getdict('SITE_COOKIES'),
            callback=self.parse,
            meta={'dont_merge_cookies': True},
            headers=headers
        )

    def parse(self, response):
        html = response.body.decode('utf-8', errors='ignore')
        # 打印起始页面的 HTML 代码
        # print("起始页面的 HTML 代码1:")
        # print(html)
        # print("起始页面的 HTML 代码2:")

        # if "ChainFeeds Newsletter" not in response.text:
        #     self.logger.error("Cookie登录验证失败")
        #     return

        # 使用 CSS 和 XPath 混合选择器提取文章链接
        links = response.css(
            'a.pencraft.pc-reset.color-pub-primary-text-NyXPlw.font-pub-headings-FE5byy.clamp-y7pNm8.clamp-3-lxFDfR.reset-IxiVJZ').xpath(
            '@href').getall()
        print(links)

        headers = {
            "authority": "substack.chainfeeds.xyz",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "max-age=0",
            "cookie": "ab_experiment_sampled=%22false%22; ab_testing_id=%220449f7d4-6942-4423-b654-25ba102c263d%22; ajs_anonymous_id=%22d5a13b83-6cca-46e4-8a5f-b5e4ca3ecab4%22; cookie_storage_key=556f216f-0492-49c4-9067-354c338a4d8f; _gcl_au=1.1.1297430761.1742978752; intro_popup_last_hidden_at=2025-03-26T09:11:50.743Z; connect.sid=s%3An31pDuw9MZrBACcZhLx7XqcSs6qhjqS5.hLXJdjN7VxHutBDNkexrynSUtFwQEnc%2FvUHVCGJSPsA; ajs_anonymous_id=%228eea04c2-deb8-466a-b555-05de8ea34307%22; visit_id=%7B%22id%22%3A%2250187c27-5f30-4f85-87a3-cc4dd39ef87c%22%2C%22timestamp%22%3A%222025-04-02T16%3A24%3A43.839Z%22%7D; __cf_bm=gzvg93IS8OMV2zvj5p7ufAYd03BXDKU.DHlPBAk1TTE-1743611084-1.0.1.1-iAVF0vtoUN4.nKfpKftx7qJnSwP7rpaUiPLsRWeGz3yfSQh4EFTZS6aXR9tHGw4ApKkbyZhAMmH6vQDujkyO4VH5wX1QBldLOVCemGydtiU; AWSALBTG=QeviN/XpqKzRKprYG76JDvOoi6lGBGmBkSaTraJTIWRO1iGx7jxeVjOfP4pVkoJsTDhyaaZ38Zhcjp8YXObqZj+iZv5UcTebm03k3kOh9JcVaKE/8IzXoKqDlD3oStGygusUbfio8q7Kz3mKnwcULl1oxWakGBlNm8gr04KulAt1; AWSALBTGCORS=QeviN/XpqKzRKprYG76JDvOoi6lGBGmBkSaTraJTIWRO1iGx7jxeVjOfP4pVkoJsTDhyaaZ38Zhcjp8YXObqZj+iZv5UcTebm03k3kOh9JcVaKE/8IzXoKqDlD3oStGygusUbfio8q7Kz3mKnwcULl1oxWakGBlNm8gr04KulAt1; _dd_s=rum=0&expire=1743612603583",
            "if-none-match": 'W/"41-JUlMLVVaXzVvwvkqWvy0XD2aODQ"',
            "priority": "u=1, i",
            "referer": "https://substack.chainfeeds.xyz/p/prozktls",
            "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }

        for relative_url in links[:5]:  # 取最新5篇文章
            if relative_url:
                full_url = urljoin(self.start_url, relative_url)
                yield response.follow(
                    url=full_url,
                    callback=self.parse_article,
                    headers=headers
                )

    def parse_article(self, response):
        """解析文章详情页"""
        # 打印文章详情页的 HTML 代码
        # print("文章详情页的 HTML 代码:")
        # print(response.text)

        current_url = response.url

        # 检查是否为新内容
        if self.last_url and current_url == self.last_url:
            self.logger.info("检测到重复URL: %s", current_url)
            return

        self.last_url = current_url

        from ..items import SubstackItem
        item = SubstackItem()
        # 提取文章时间
        time_element = response.css('div.pc-display-flex.pc-gap-4 > div.meta-EgzBVA:first-child::text').get()
        item["time"]=time_element
        item['url'] = current_url
        item['title'] = response.css('h1.post-title').xpath('text()').get()
        item['author'] = 'ChainfeedsPro前沿'
        item['content'] = '\n'.join(response.css('div.post-content p').xpath('text()').getall())
        print(item)
        yield item
