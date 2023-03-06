from http import HTTPStatus

from api.models.progress_film import ProgressFilmModel
from fastapi import APIRouter, Depends, HTTPException
from services.auth import JWTBearer
from services.progress_film import progress

router = APIRouter(prefix="/ugc_api/v1", tags=["progress"])


@router.post("/progress-film")
async def post_event(
    progress_film: ProgressFilmModel,
    user_id=Depends(JWTBearer()),
):
    try:
        await progress(user_id, progress_film)
        return HTTPStatus.OK
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=e.args[0].str())
