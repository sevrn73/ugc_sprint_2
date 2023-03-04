from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """
    Настройки проекта
    """

    KAFKA_BROKER_HOST = Field("ugc.kafka", env="KAFKA_BROKER_HOST")
    KAFKA_BROKER_PORT = Field(9092, env="KAFKA_BROKER_PORT")
    KAFKA_BROKER_URL = f"{KAFKA_BROKER_HOST}:{KAFKA_BROKER_PORT}"
    KAFKA_TOPIC_PREFIX = "views"
    clickhouse_host: str = Field("localhost", env="CLICKHOUSE_HOST")
    clickhouse_port: str = Field(9000, env="CLICKHOUSE_PORT")


settings = Settings()
