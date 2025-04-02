import requests
import json
from itemadapter import ItemAdapter


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