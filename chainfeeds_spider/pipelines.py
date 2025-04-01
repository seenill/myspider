# pipelines.py
import json

from confluent_kafka import Producer

class KafkaPipeline:
    def __init__(self, servers, topic):
        self.producer = Producer({'bootstrap.servers': servers})
        self.topic = topic

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            servers=crawler.settings.get('KAFKA_SERVERS'),
            topic=crawler.settings.get('KAFKA_TOPIC')
        )

    def process_item(self, item, spider):
        self.producer.send(self.topic, value=dict(item))
        return item

# settings.py
ITEM_PIPELINES = {
    'chainfeeds_spider.FeishuPipeline': 300,
    'your_project.pipelines.KafkaPipeline': 800,
}
KAFKA_SERVERS = ['kafka-server:9092']
KAFKA_TOPIC = 'chainfeeds-articles'