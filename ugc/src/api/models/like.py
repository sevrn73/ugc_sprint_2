from datetime import datetime
from typing import Optional

from api.models.basemodel import OrjsonBaseModel


class LikeModel(OrjsonBaseModel):
    """Модель лайков."""

    user_id: str
    film_id: str
    score: int
    timestamp: Optional[datetime] = None
