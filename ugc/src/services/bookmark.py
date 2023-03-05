from datetime import datetime
from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException

from api.models.bookmark import BookmarkModel
from broker.mongo import mongo
from core.config import settings


async def get_bookmarks_list(
    user_id: str,
    limit: int = settings.DEFAULT_LIMIT,
    offset: int = settings.DEFAULT_OFFSET,
) -> list[BookmarkModel]:
    """Получить список закладок"""
    data = await mongo.find(
        settings.MONGO_COLLECTION_BOOKMARK, {"user_id": user_id}, limit=limit, offset=offset
    )
    return [BookmarkModel(**item) async for item in data]


async def get_bookmark(user_id: str, film_id: str) -> Optional[BookmarkModel]:
    """Получить одну закладку"""
    data = await mongo.find_one(
        settings.MONGO_COLLECTION_BOOKMARK, {"user_id": user_id, "film_id": film_id}
    )
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return BookmarkModel(**data)


async def create_bookmark(user_id: str, film_id: str) -> BookmarkModel:
    """Создать закладку"""
    data = await mongo.find_one(
        settings.MONGO_COLLECTION_BOOKMARK, {"user_id": user_id, "film_id": film_id}
    )
    if data:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    data = BookmarkModel(user_id=user_id, film_id=film_id, timestamp=datetime.now())
    await mongo.insert(settings.MONGO_COLLECTION_BOOKMARK, data.dict())
    return data


async def remove_bookmark(user_id: str, film_id: str) -> None:
    """Удалить закладку"""
    data = await mongo.find_one(
        settings.MONGO_COLLECTION_BOOKMARK, {"user_id": user_id, "film_id": film_id}
    )
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    await mongo.delete(
        settings.MONGO_COLLECTION_BOOKMARK, {"user_id": user_id, "film_id": film_id}
    )
