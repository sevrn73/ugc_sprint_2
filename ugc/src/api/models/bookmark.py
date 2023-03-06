from datetime import datetime
from typing import Optional

from api.models.basemodel import OrjsonBaseModel


class BookmarkModel(OrjsonBaseModel):
    """Модель закладок."""

    user_id: str
    film_id: str
    timestamp: Optional[datetime] = None
