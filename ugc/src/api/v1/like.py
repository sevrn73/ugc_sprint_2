from http import HTTPStatus
from typing import Any, List

from api.models.like import LikeModel
from fastapi import APIRouter, Depends
from services import like
from services.auth import JWTBearer

router = APIRouter(prefix="/ugc_api/v1", tags=["likes"])


@router.get("/likes", response_model=List[LikeModel])
async def get_likes_list(
    limit: int = 10,
    offset: int = 0,
    user_id=Depends(JWTBearer()),
) -> Any:
    """
    Список лайков
    """
    return await like.get_likes_list(user_id=user_id, limit=limit, offset=offset)


@router.post("/like/{film_id}", response_model=LikeModel)
async def create_like(
    film_id: str,
    user_id=Depends(JWTBearer()),
) -> Any:
    """
    Создать лайк
    """
    return await like.create_like(user_id=user_id, film_id=film_id, score=10)


@router.post("/dislike/{film_id}", response_model=LikeModel)
async def create_dislike(
    film_id: str,
    user_id=Depends(JWTBearer()),
) -> Any:
    """
    Создать дизлайк
    """
    return await like.create_like(user_id=user_id, film_id=film_id, score=0)


@router.get("/like/{film_id}", response_model=LikeModel)
async def read_category(
    film_id: str,
    user_id=Depends(JWTBearer()),
) -> Any:
    """
    Получить лайк
    """
    like_confirm = await like.get_like(user_id=user_id, film_id=film_id)
    return like_confirm


@router.delete("/like/{film_id}", response_model=str)
async def delete_category(
    film_id: str,
    user_id=Depends(JWTBearer()),
) -> Any:
    """
    Удалить лайк
    """
    await like.remove_like(user_id=user_id, film_id=film_id)
    return HTTPStatus.OK
