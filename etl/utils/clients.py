import json

from clickhouse_driver import Client
from kafka import KafkaConsumer

from utils.backoff import backoff
from utils.settings import settings


def get_kafka() -> KafkaConsumer:
    kafka_consumer = KafkaConsumer(
        settings.KAFKA_TOPIC_PREFIX,
        group_id="timestamp_movie",
        bootstrap_servers=f"{settings.KAFKA_BROKER_HOST}:{settings.KAFKA_BROKER_PORT}",
        enable_auto_commit=False,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )
    return kafka_consumer


def close_kafka_connection(kafka_consumer: KafkaConsumer) -> None:
    kafka_consumer.close()


def get_clickhouse() -> Client:
    clickhouse_client = Client(host=settings.clickhouse_host, port=settings.clickhouse_port)
    return clickhouse_client


def close_clickhouse_connection(clickhouse_client: Client) -> None:
    clickhouse_client.disconnect()
