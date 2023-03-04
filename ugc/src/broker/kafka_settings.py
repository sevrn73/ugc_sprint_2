from aiokafka import AIOKafkaProducer

from core.config import settings


class KafkaProducer:
    """
    Продьюсер Kafka
    """

    kafka_producer = None

    async def get_producer(self):
        self.kafka_producer = AIOKafkaProducer(
            bootstrap_servers=f"{settings.KAFKA_BROKER_HOST}:{settings.KAFKA_BROKER_PORT}"
        )
        await self.kafka_producer.start()

    async def stop_producer(
        self,
    ):
        await self.kafka_producer.start()


kafka = KafkaProducer()
