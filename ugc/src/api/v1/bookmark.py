from http import HTTPStatus
from typing import Any, List

from api.models.bookmark import BookmarkModel
from fastapi import APIRouter, Depends
from services import bookmark
from services.auth import JWTBearer

router = APIRouter(prefix="/ugc_api/v1", tags=["bookmarks"])


@router.get("/bookmarks", response_model=List[BookmarkModel])
async def get_bookmarks_list(
    limit: int = 10,
    offset: int = 0,
    user_id=Depends(JWTBearer()),
) -> Any:
    """
    Список закладок
    """
    return await bookmark.get_bookmarks_list(user_id=user_id, limit=limit, offset=offset)


@router.post("/bookmark/{film_id}", response_model=BookmarkModel)
async def create_bookmark(
    film_id: str,
    user_id=Depends(JWTBearer()),
) -> Any:
    """
    Создать закладку
    """
    return await bookmark.create_bookmark(user_id=user_id, film_id=film_id)


@router.get("/bookmark/{film_id}", response_model=BookmarkModel)
async def read_category(
    film_id: str,
    user_id=Depends(JWTBearer()),
) -> Any:
    """
    Получить закладку
    """
    bookm = await bookmark.get_bookmark(user_id=user_id, film_id=film_id)
    return bookm


@router.delete("/bookmark/{film_id}", response_model=str)
async def delete_category(
    film_id: str,
    user_id=Depends(JWTBearer()),
) -> Any:
    """
    Удалить закладку
    """
    await bookmark.remove_bookmark(user_id=user_id, film_id=film_id)
    return HTTPStatus.OK
