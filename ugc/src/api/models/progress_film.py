import uuid

from pydantic import Field

from api.models.basemodel import OrjsonBaseModel


class ProgressFilmModel(OrjsonBaseModel):
    movie_id: uuid.UUID = Field(title="идентификатор фильма")
    timestamp_movie: int = Field(title="прогресс просмотра фильма")
