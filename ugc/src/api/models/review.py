from datetime import datetime
from typing import Optional

from api.models.basemodel import OrjsonBaseModel

class ReviewModel(OrjsonBaseModel):
    """Модель рецензии."""
    user_id: str
    film_id: str
    text: str
    timestamp: Optional[datetime] = None
