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

cookie_str = 'ab_experiment_sampled=%22false%22; ab_testing_id=%220449f7d4-6942-4423-b654-25ba102c263d%22; ajs_anonymous_id=%22d5a13b83-6cca-46e4-8a5f-b5e4ca3ecab4%22; cookie_storage_key=556f216f-0492-49c4-9067-354c338a4d8f; _gcl_au=1.1.1297430761.1742978752; intro_popup_last_hidden_at=2025-03-26T09:11:50.743Z; connect.sid=s%3An31pDuw9MZrBACcZhLx7XqcSs6qhjqS5.hLXJdjN7VxHutBDNkexrynSUtFwQEnc%2FvUHVCGJSPsA; ajs_anonymous_id=%228eea04c2-deb8-466a-b555-05de8ea34307%22; visit_id=%7B%22id%22%3A%2250187c27-5f30-4f85-87a3-cc4dd39ef87c%22%2C%22timestamp%22%3A%222025-04-02T16%3A24%3A43.839Z%22%7D; __cf_bm=gzvg93IS8OMV2zvj5p7ufAYd03BXDKU.DHlPBAk1TTE-1743611084-1.0.1.1-iAVF0vtoUN4.nKfpKftx7qJnSwP7rpaUiPLsRWeGz3yfSQh4EFTZS6aXR9tHGw4ApKkbyZhAMmH6vQDujkyO4VH5wX1QBldLOVCemGydtiU; AWSALBTG=QeviN/XpqKzRKprYG76JDvOoi6lGBGmBkSaTraJTIWRO1iGx7jxeVjOfP4pVkoJsTDhyaaZ38Zhcjp8YXObqZj+iZv5UcTebm03k3kOh9JcVaKE/8IzXoKqDlD3oStGygusUbfio8q7Kz3mKnwcULl1oxWakGBlNm8gr04KulAt1; AWSALBTGCORS=QeviN/XpqKzRKprYG76JDvOoi6lGBGmBkSaTraJTIWRO1iGx7jxeVjOfP4pVkoJsTDhyaaZ38Zhcjp8YXObqZj+iZv5UcTebm03k3kOh9JcVaKE/8IzXoKqDlD3oStGygusUbfio8q7Kz3mKnwcULl1oxWakGBlNm8gr04KulAt1; _dd_s=rum=0&expire=1743612603583'
SITE_COOKIES = {}
for cookie in cookie_str.split('; '):
    if cookie:
        key, value = cookie.split('=', 1)
        SITE_COOKIES[key] = value


SCHEDULE_INTERVAL = 300  # 5分钟

EXTENSIONS = {
    'chainfeeds_kafka_project.extensions.SchedulerExtension': 500,
}
#kafka
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'  # Kafka服务器地址
KAFKA_TOPIC = 'test-topic'  # 目标主题名称
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
# ITEM_PIPELINES = {
#    "chainfeeds_kafka_project.pipelines.ChainfeedsKafkaProjectPipeline": 300,
# }
ITEM_PIPELINES = {
    'chainfeeds_kafka_project.pipelines.KafkaPipeline': 300,
}

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
