import uuid

from api.models.basemodel import OrjsonBaseModel
from pydantic import Field


class ProgressFilmModel(OrjsonBaseModel):
    movie_id: uuid.UUID = Field(title="идентификатор фильма")
    timestamp_movie: int = Field(title="прогресс просмотра фильма")
