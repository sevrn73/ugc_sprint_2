from datetime import datetime
from http import HTTPStatus
from typing import List, Optional

from api.models.like import LikeModel
from broker.mongo import mongo_client
from core.config import settings
from fastapi import HTTPException


async def get_likes_list(
    user_id: str,
    limit: int = settings.DEFAULT_LIMIT,
    offset: int = settings.DEFAULT_OFFSET,
) -> List[LikeModel]:
    """Получить список лайков"""
    data = await mongo_client.find(settings.MONGO_COLLECTION_LIKE, {"user_id": user_id}, limit=limit, offset=offset)
    return [LikeModel(**item) async for item in data]


async def get_like(user_id: str, film_id: str) -> Optional[LikeModel]:
    """Получить один лайк"""
    data = await mongo_client.find_one(settings.MONGO_COLLECTION_LIKE, {"user_id": user_id, "film_id": film_id})
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return LikeModel(**data)


async def create_like(user_id: str, film_id: str, score: int) -> LikeModel:
    """Создать лайк"""
    data = await mongo_client.find_one(settings.MONGO_COLLECTION_LIKE, {"user_id": user_id, "film_id": film_id})
    if data:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    data = LikeModel(user_id=user_id, film_id=film_id, score=score, timestamp=datetime.now())
    await mongo_client.insert(settings.MONGO_COLLECTION_LIKE, data.dict())
    return data


async def remove_like(user_id: str, film_id: str) -> None:
    """Удалить лайк"""
    data = await mongo_client.find_one(settings.MONGO_COLLECTION_LIKE, {"user_id": user_id, "film_id": film_id})
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    await mongo_client.delete(settings.MONGO_COLLECTION_LIKE, {"user_id": user_id, "film_id": film_id})
