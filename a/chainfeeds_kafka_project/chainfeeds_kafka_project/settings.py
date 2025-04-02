# Scrapy settings for chainfeeds_kafka_project project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "chainfeeds_kafka_project"

SPIDER_MODULES = ["chainfeeds_kafka_project.spiders"]
NEWSPIDER_MODULE = "chainfeeds_kafka_project.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
LOG_LEVEL = "WARNING"

FEISHU_WEBHOOK = 'https://open.feishu.cn/...你的webhook地址...'

cookie_str = 'ab_experiment_sampled=%22false%22; ab_testing_id=%220449f7d4-6942-4423-b654-25ba102c263d%22; ajs_anonymous_id=%22d5a13b83-6cca-46e4-8a5f-b5e4ca3ecab4%22; cookie_storage_key=556f216f-0492-49c4-9067-354c338a4d8f; _gcl_au=1.1.1297430761.1742978752; intro_popup_last_hidden_at=2025-03-26T09:11:50.743Z; connect.sid=s%3An31pDuw9MZrBACcZhLx7XqcSs6qhjqS5.hLXJdjN7VxHutBDNkexrynSUtFwQEnc%2FvUHVCGJSPsA; ajs_anonymous_id=%228eea04c2-deb8-466a-b555-05de8ea34307%22; __cf_bm=Zc6bIZ4yHgRWKwhl5tsffXkmW.vuFY.hkfj7DDmh6Wc-1743604555-1.0.1.1-UzZbQoo9.GYpRQ7f3rKKDzxbKIiBegdXcei5yMIv2IGD8bUSTZJLwACbBeWTEqXVIGV.0Km2wKmqv.pNOW8jUE2rmke9DMKK1UWHB51uJVE; visit_id=%7B%22id%22%3A%22a702ec8b-23da-46fa-86f8-6af3b1c6f585%22%2C%22timestamp%22%3A%222025-04-02T14%3A37%3A47.714Z%22%7D; AWSALBTG=5xXQSMA81yy2SjwwzzFmRDSTCASaE5uzMJ/igVGy4I4bcUkgAYLwx4Uwd0dOfIbl80Cd+W6F3OZ37+0sfinv+lw95A3Oen9r1rHaKbKq3sO47uOBte7FiNvDqVwaeLdnQlmE1DP0feTBoN85T1XwpX1vyMtYVn2/+giVdG6EFwQk; AWSALBTGCORS=5xXQSMA81yy2SjwwzzFmRDSTCASaE5uzMJ/igVGy4I4bcUkgAYLwx4Uwd0dOfIbl80Cd+W6F3OZ37+0sfinv+lw95A3Oen9r1rHaKbKq3sO47uOBte7FiNvDqVwaeLdnQlmE1DP0feTBoN85T1XwpX1vyMtYVn2/+giVdG6EFwQk; _dd_s=rum=0&expire=1743605581460'
SITE_COOKIES = {}
for cookie in cookie_str.split('; '):
    if cookie:
        key, value = cookie.split('=', 1)
        SITE_COOKIES[key] = value


SCHEDULE_INTERVAL = 300  # 5分钟

EXTENSIONS = {
    'chainfeeds_kafka_project.extensions.SchedulerExtension': 500,
}
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "chainfeeds_kafka_project.middlewares.ChainfeedsKafkaProjectSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "chainfeeds_kafka_project.middlewares.ChainfeedsKafkaProjectDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "chainfeeds_kafka_project.pipelines.ChainfeedsKafkaProjectPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
