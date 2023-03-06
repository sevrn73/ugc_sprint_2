from http import HTTPStatus
from typing import Any, List

from api.models.review import ReviewModel
from fastapi import APIRouter, Depends
from services import review
from services.auth import JWTBearer

router = APIRouter(prefix="/ugc_api/v1", tags=["reviews"])


@router.get("/reviews", response_model=List[ReviewModel])
async def get_reviews_list(
    limit: int = 10,
    offset: int = 0,
    user_id=Depends(JWTBearer()),
) -> Any:
    """
    Список рецензий
    """
    return await review.get_reviews_list(user_id=user_id, limit=limit, offset=offset)


@router.post("/review/{film_id}", response_model=ReviewModel)
async def create_review(
    film_id: str,
    text: str,
    user_id=Depends(JWTBearer()),
) -> Any:
    """
    Создать рецензию
    """
    return await review.create_review(user_id=user_id, film_id=film_id, text=text)


@router.get("/review/{film_id}", response_model=ReviewModel)
async def read_category(
    film_id: str,
    user_id=Depends(JWTBearer()),
) -> Any:
    """
    Получить рецензию
    """
    rew = await review.get_review(user_id=user_id, film_id=film_id)
    return rew


@router.delete("/review/{film_id}", response_model=HTTPStatus)
async def delete_category(
    film_id: str,
    user_id=Depends(JWTBearer()),
) -> Any:
    """
    Удалить рецензию
    """
    await review.remove_review(user_id=user_id, film_id=film_id)
    return HTTPStatus.OK
