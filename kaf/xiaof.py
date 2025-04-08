import json
import logging
import time
import hmac
import hashlib
import requests
from confluent_kafka import Consumer, KafkaError
import os
from dotenv import load_dotenv
# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# 加载环境变量（可根据实际情况修改）
load_dotenv()

# Kafka 配置
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
KAFKA_CONSUMER_GROUP = os.getenv('KAFKA_CONSUMER_GROUP', 'default_consumer_group')

# 飞书配置
FEISHU_WEBHOOK_URL = os.getenv('FEISHU_WEBHOOK_URL')
FEISHU_SECRET = os.getenv('FEISHU_SECRET')


def calculate_signature(timestamp):
    """
    计算飞书签名
    """
    try:
        if not FEISHU_SECRET:
            logging.error("FEISHU_SECRET 未配置或为空")
            return ""
        string_to_sign = f'{timestamp}\n{FEISHU_SECRET}'
        hmac_code = hmac.new(
            key=FEISHU_SECRET.encode('utf-8'),
            msg=string_to_sign.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        signature = hmac_code.hex()
        return signature
    except Exception as e:
        logging.error(f"签名计算错误：{e}")
        return ""


def send_to_feishu(message):
    try:
        timestamp = str(int(time.time()))
        signature = calculate_signature(timestamp)
        data = {
            "msg_type": "interactive",
            "card": {
                "config": {
                    "wide_screen_mode": True
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "content": f"标题: {message.get('title', '')}\n作者: {message.get('author', '')}\n内容: {message.get('content', '')}",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "tag": "action",
                        "actions": [
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "查看原文"
                                },
                                "type": "default",
                                "url": message.get('url', "")
                            }
                        ]
                    }
                ],
                "header": {
                    "title": {
                        "content": "Kafka 消息推送",
                        "tag": "plain_text"
                    }
                }
            },
            "timestamp": timestamp,
            "sign": signature
        }
        response = requests.post(FEISHU_WEBHOOK_URL, json=data)
        if response.status_code != 200:
            logging.error(f"发送到飞书失败，状态码: {response.status_code}，响应内容: {response.text}")
        else:
            result = response.json()
            if result["code"] != 0:
                logging.error(f"消息发送到飞书后返回错误，错误码: {result['code']}，错误信息: {result['msg']}")
            else:
                logging.info(f"消息已成功发送到飞书：{data}")
    except requests.RequestException as e:
        logging.error(f"发送消息到飞书时发生网络请求异常: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"解析飞书响应的 JSON 数据时出错: {e}")
    except Exception as e:
        logging.error(f"发送消息到飞书时出现未知错误: {e}")


def consume_from_kafka():
    conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': KAFKA_CONSUMER_GROUP,
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(conf)
    consumer.subscribe([KAFKA_TOPIC])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logging.info(f"Reached end of partition: {msg.topic()} [{msg.partition()}]")
                else:
                    logging.error(f"Kafka 消费错误: {msg.error()}")
            else:
                try:
                    message = json.loads(msg.value().decode('utf-8'))
                    send_to_feishu(message)
                except json.JSONDecodeError as e:
                    logging.error(f"解析 Kafka 消息的 JSON 数据时出错: {e}")
    except KeyboardInterrupt:
        logging.info("程序被手动终止，正在关闭 Kafka 消费者...")
    finally:
        consumer.close()


if __name__ == "__main__":
    if not KAFKA_BOOTSTRAP_SERVERS or not KAFKA_TOPIC or not FEISHU_WEBHOOK_URL or not FEISHU_SECRET:
        logging.error("Kafka 或飞书的必要配置项未正确设置，请检查.env 文件。")
    else:
        consume_from_kafka()