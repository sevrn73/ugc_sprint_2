"""
Модуль ETL процесса
"""
from utils.logger import logger
import time
import uuid

from clickhouse_driver import Client
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

from utils.backoff import backoff
from utils.clients import get_kafka, get_clickhouse, close_clickhouse_connection, close_kafka_connection


def create_table(client: Client) -> None:
    """
    Создание таблицы в Clickhouse

    :param client: клиент Clickhouse
    """
    client.execute(
        """
        CREATE TABLE IF NOT EXISTS views (
            id String,
            user_id String,
            movie_id String,
            timestamp_movie Int64,
            time Int64
        ) Engine=MergeTree() ORDER BY id
        """
    )


@backoff()
def load_to_clickhouse(clickhouse_client: Client, data: list) -> None:
    """
    Загрузка в Clickhouse

    :param client: клиент Clickhouse
    :param data: данные для переноса в Clickhouse
    """
    clickhouse_client.execute(
        "INSERT INTO views (id, user_id, movie_id, timestamp_movie, time) VALUES",
        data,
    )


def etl(kafka_consumer: KafkaConsumer, clickhouse_client: Client) -> None:
    """
    ETL процесс, переносит данные из Kafka в Clickhouse

    :param kafka_consumer: консьюмер кафки
    :param clickhouse_client: клиент Clickhouse
    """
    data = []
    start = time.time()
    for message in kafka_consumer:
        msg = (
            str(uuid.uuid4()),
            *str(message.key.decode("utf-8")).split(":"),
            message.value["timestamp_movie"],
            message.timestamp,
        )
        data.append(msg)
        if (len(data) >= 1) or (time.time() - start >= 60):
            load_to_clickhouse(clickhouse_client, data)
            data = []
            start = time.time()
            kafka_consumer.commit()


def main() -> None:
    """
    Основная функция ETL процесса
    """
    while True:
        try:
            kafka_consumer = get_kafka()
            clickhouse_client = get_clickhouse()
            create_table(clickhouse_client)
            etl(kafka_consumer, clickhouse_client)
        except NoBrokersAvailable:
            logger.error("Error connecting to kafka")

        finally:
            close_kafka_connection(kafka_consumer)
            close_clickhouse_connection(clickhouse_client)

        time.sleep(1)


if __name__ == "__main__":
    main()
