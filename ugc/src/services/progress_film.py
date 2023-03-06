from api.models.progress_film import ProgressFilmModel
from broker.kafka_settings import kafka
from core.config import settings


async def progress(user_id: str, progress_film: ProgressFilmModel):
    """Отправить нотификацию в кафку"""
    await kafka.kafka_producer.send(
        topic=settings.KAFKA_TOPIC_PREFIX,
        value=progress_film.json().encode(),
        key=f"{user_id}:{progress_film.movie_id}".encode(),
    )
