from http import HTTPStatus
from fastapi import Depends, HTTPException, APIRouter
from core.config import settings
from broker.kafka_settings import kafka
from api.models.progress_film import ProgressFilmModel
from services.auth import JWTBearer

router = APIRouter(prefix="/ugc_api/v1", tags=["progress_film"])


@router.post("/progress_film/")
async def post_event(
    progress_film: ProgressFilmModel,
    user_id=Depends(JWTBearer()),
):
    try:
        await kafka.kafka_producer.send(
            topic=settings.KAFKA_TOPIC_PREFIX,
            value=progress_film.json().encode(),
            key=f"{user_id}:{progress_film.movie_id}".encode(),
        )
        return HTTPStatus.OK
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=e.args[0].str())
