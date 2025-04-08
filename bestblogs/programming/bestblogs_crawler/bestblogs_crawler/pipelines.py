import json
from itemadapter import ItemAdapter
from confluent_kafka import Producer
from scrapy.utils import spider


class KafkaPipeline:
    """Kafka消息推送管道"""

    def __init__(self, bootstrap_servers, topic):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = Producer({
            'bootstrap.servers': self.bootstrap_servers,
            'client.id': 'scrapy-kafka-producer'
        })

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            bootstrap_servers=crawler.settings.get('KAFKA_BOOTSTRAP_SERVERS'),
            topic=crawler.settings.get('KAFKA_TOPIC')
        )

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        message = {
            'url': adapter['url'],
            'title': adapter['title'],
            'author': adapter['author'],
            'content': adapter['content']
        }

        try:
            self.producer.produce(
                self.topic,
                key=adapter['url'].encode('utf-8'),
                value=json.dumps(message).encode('utf-8'),
                callback=self.delivery_report
            )
            self.producer.poll(0)
            spider.logger.info(f"Kafka消息发送成功: {adapter['url']}")
        except Exception as e:
            spider.logger.error(f"Kafka消息发送失败: {str(e)}")

        return item

    # def close_spider(self, spider):
    #     self.producer.flush()
    #     self.producer.close()

    def delivery_report(self, err, msg):
        """消息发送回调函数"""
        if err is not None:
            spider.logger.error(f"Kafka消息发送失败: {err}")
        else:
            spider.logger.debug(f"Kafka消息已送达: {msg.topic()} [{msg.partition()}]")