from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """
    Настройки проекта
    """

    KAFKA_BROKER_HOST = Field("ugc.kafka", env="KAFKA_BROKER_HOST")
    KAFKA_BROKER_PORT = Field(9092, env="KAFKA_BROKER_PORT")
    KAFKA_TOPIC_PREFIX = "views"
    VERIFY_JWT_URL = Field("http://nginx:80/v1/check_perm", env="VERIFY_JWT_URL")

    password: str = Field("", env="POSTGRES_PASSWORD")
    ugc_host: str = Field("0.0.0.0", env="DB_HOST")
    ugc_port: int = Field(8001, env="DB_PORT")
    LOGSTASH_HOST: str = Field("logstash", env="LOGSTASH_HOST")
    LOGSTASH_PORT: int = Field(5044, env="LOGSTASH_PORT")

    # MONGO_HOST: str = Field("localhost", env="MONGO_HOST")
    MONGO_HOST: str = Field("mongos1", env="MONGO_HOST")
    MONGO_PORT: int = Field(27017, env="MONGO_PORT")
    MONGO_DB: str = Field("ugc_db", env="MONGO_DB")
    MONGO_COLLECTION_LIKE: str = Field("likes", env="MONGO_COLLECTION_LIKE")
    MONGO_COLLECTION_REVIEW: str = Field("reviews", env="MONGO_COLLECTION_REVIEW")
    MONGO_COLLECTION_BOOKMARK: str = Field("bookmarks", env="MONGO_COLLECTION_BOOKMARK")
    DEFAULT_LIMIT: int = Field(10, env="DEFAULT_LIMIT")
    DEFAULT_OFFSET: int = Field(0, env="DEFAULT_OFFSET")
    SENTRY_DSN: str = Field("", env="SENTRY_DSN")


settings = Settings()
