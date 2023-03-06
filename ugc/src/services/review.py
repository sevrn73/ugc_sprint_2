from datetime import datetime
from http import HTTPStatus
from typing import List, Optional

from api.models.review import ReviewModel
from broker.mongo import mongo
from core.config import settings
from fastapi import HTTPException


async def get_reviews_list(
    user_id: str,
    limit: int = settings.DEFAULT_LIMIT,
    offset: int = settings.DEFAULT_OFFSET,
) -> List[ReviewModel]:
    """Получить список рецензий"""
    data = await mongo.find(settings.MONGO_COLLECTION_REVIEW, {"user_id": user_id}, limit=limit, offset=offset)
    return [ReviewModel(**item) async for item in data]


async def get_review(user_id: str, film_id: str) -> Optional[ReviewModel]:
    """Получить одну рецензию"""
    data = await mongo.find_one(settings.MONGO_COLLECTION_REVIEW, {"user_id": user_id, "film_id": film_id})
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return ReviewModel(**data)


async def create_review(user_id: str, film_id: str, text: str) -> ReviewModel:
    """Создать рецензию"""
    data = await mongo.find_one(settings.MONGO_COLLECTION_REVIEW, {"user_id": user_id, "film_id": film_id})
    if data:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    data = ReviewModel(user_id=user_id, film_id=film_id, text=text, timestamp=datetime.now())
    await mongo.insert(settings.MONGO_COLLECTION_REVIEW, data.dict())
    return data


async def remove_review(user_id: str, film_id: str) -> None:
    """Удалить рецензию"""
    data = await mongo.find_one(settings.MONGO_COLLECTION_REVIEW, {"user_id": user_id, "film_id": film_id})
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    await mongo.delete(settings.MONGO_COLLECTION_REVIEW, {"user_id": user_id, "film_id": film_id})
