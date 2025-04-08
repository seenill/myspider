import scrapy
from urllib.parse import urljoin


class ChainfeedsSpider(scrapy.Spider):
    name = "chainfeeds"
    allowed_domains = ["substack.chainfeeds.xyz"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_url = None  # 用于存储上一次的 URL
        self.start_url = kwargs.get('start_url', 'https://substack.chainfeeds.xyz/s/daily')

    def start_requests(self):
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 'ab_experiment_sampled=%22false%22; ab_testing_id=%220449f7d4-6942-4423-b654-25ba102c263d%22; ajs_anonymous_id=%22d5a13b83-6cca-46e4-8a5f-b5e4ca3ecab4%22; cookie_storage_key=556f216f-0492-49c4-9067-354c338a4d8f; _gcl_au=1.1.1297430761.1742978752; intro_popup_last_hidden_at=2025-03-26T09:11:50.743Z; connect.sid=s%3An31pDuw9MZrBACcZhLx7XqcSs6qhjqS5.hLXJdjN7VxHutBDNkexrynSUtFwQEnc%2FvUHVCGJSPsA; ajs_anonymous_id=%228eea04c2-deb8-466a-b555-05de8ea34307%22; __cf_bm=Zc6bIZ4yHgRWKwhl5tsffXkmW.vuFY.hkfj7DDmh6Wc-1743604555-1.0.1.1-UzZbQoo9.GYpRQ7f3rKKDzxbKIiBegdXcei5yMIv2IGD8bUSTZJLwACbBeWTEqXVIGV.0Km2wKmqv.pNOW8jUE2rmke9DMKK1UWHB51uJVE; visit_id=%7B%22id%22%3A%22a702ec8b-23da-46fa-86f8-6af3b1c6f585%22%2C%22timestamp%22%3A%222025-04-02T14%3A37%3A47.714Z%22%7D; AWSALBTG=5xXQSMA81yy2SjwwzzFmRDSTCASaE5uzMJ/igVGy4I4bcUkgAYLwx4Uwd0dOfIbl80Cd+W6F3OZ37+0sfinv+lw95A3Oen9r1rHaKbKq3sO47uOBte7FiNvDqVwaeLdnQlmE1DP0feTBoN85T1XwpX1vyMtYVn2/+giVdG6EFwQk; AWSALBTGCORS=5xXQSMA81yy2SjwwzzFmRDSTCASaE5uzMJ/igVGy4I4bcUkgAYLwx4Uwd0dOfIbl80Cd+W6F3OZ37+0sfinv+lw95A3Oen9r1rHaKbKq3sO47uOBte7FiNvDqVwaeLdnQlmE1DP0feTBoN85T1XwpX1vyMtYVn2/+giVdG6EFwQk; _dd_s=rum=0&expire=1743605581460',
            'if-none-match': 'W/"1704-iprIok+fMiqkRO6RQHOX+MpcLW8"',
            'priority': 'u=1, i',
            'referer': 'https://substack.chainfeeds.xyz/s/daily',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        }

        yield scrapy.Request(
            url=self.start_url,
            cookies=self.settings.getdict('SITE_COOKIES'),
            callback=self.parse,
            meta={'dont_merge_cookies': True},
            headers=headers
        )

    def parse(self, response):
        # 打印起始页面的 HTML 代码
        # print("起始页面的 HTML 代码:")
        # print(response.text)

        if "ChainFeeds Newsletter" not in response.text:
            self.logger.error("Cookie登录验证失败")
            return

        # 使用 CSS 和 XPath 混合选择器提取文章链接
        links = response.css(
            'a.pencraft.pc-reset.color-pub-primary-text-NyXPlw.font-pub-headings-FE5byy.clamp-y7pNm8.clamp-3-lxFDfR.reset-IxiVJZ').xpath(
            '@href').getall()
        # print(links)

        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 'ab_experiment_sampled=%22false%22; ab_testing_id=%220449f7d4-6942-4423-b654-25ba102c263d%22; ajs_anonymous_id=%22d5a13b83-6cca-46e4-8a5f-b5e4ca3ecab4%22; cookie_storage_key=556f216f-0492-49c4-9067-354c338a4d8f; _gcl_au=1.1.1297430761.1742978752; intro_popup_last_hidden_at=2025-03-26T09:11:50.743Z; connect.sid=s%3An31pDuw9MZrBACcZhLx7XqcSs6qhjqS5.hLXJdjN7VxHutBDNkexrynSUtFwQEnc%2FvUHVCGJSPsA; ajs_anonymous_id=%228eea04c2-deb8-466a-b555-05de8ea34307%22; __cf_bm=Zc6bIZ4yHgRWKwhl5tsffXkmW.vuFY.hkfj7DDmh6Wc-1743604555-1.0.1.1-UzZbQoo9.GYpRQ7f3rKKDzxbKIiBegdXcei5yMIv2IGD8bUSTZJLwACbBeWTEqXVIGV.0Km2wKmqv.pNOW8jUE2rmke9DMKK1UWHB51uJVE; visit_id=%7B%22id%22%3A%22a702ec8b-23da-46fa-86f8-6af3b1c6f585%22%2C%22timestamp%22%3A%222025-04-02T14%3A37%3A47.714Z%22%7D; AWSALBTG=5xXQSMA81yy2SjwwzzFmRDSTCASaE5uzMJ/igVGy4I4bcUkgAYLwx4Uwd0dOfIbl80Cd+W6F3OZ37+0sfinv+lw95A3Oen9r1rHaKbKq3sO47uOBte7FiNvDqVwaeLdnQlmE1DP0feTBoN85T1XwpX1vyMtYVn2/+giVdG6EFwQk; AWSALBTGCORS=5xXQSMA81yy2SjwwzzFmRDSTCASaE5uzMJ/igVGy4I4bcUkgAYLwx4Uwd0dOfIbl80Cd+W6F3OZ37+0sfinv+lw95A3Oen9r1rHaKbKq3sO47uOBte7FiNvDqVwaeLdnQlmE1DP0feTBoN85T1XwpX1vyMtYVn2/+giVdG6EFwQk; _dd_s=rum=0&expire=1743605581460',
            'if-none-match': 'W/"1704-iprIok+fMiqkRO6RQHOX+MpcLW8"',
            'priority': 'u=1, i',
            'referer': 'https://substack.chainfeeds.xyz/s/daily',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
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
        time_elements = response.css('div.meta-EgzBVA')
        for element in time_elements:
            # 尝试提取中文时间
            chinese_time = element.css('font::text').get()
            if chinese_time:
                item['time'] = chinese_time.strip()
                break  # 找到第一个有效时间后停止
            # 如果中文时间不存在，尝试提取英文时间
            if not item.get('time'):
                english_time = element.xpath('text()').get()
                if english_time:
                    item['time'] = english_time.strip()
        item['url'] = current_url
        item['title'] = response.css('h1.post-title').xpath('text()').get()
        item['author'] = "Chainfeeds投研早报"#response.css('div.post-author').xpath('text()').get()
        item['content'] = '\n'.join(response.css('div.post-content p').xpath('text()').getall())
        print(item)
        yield item
