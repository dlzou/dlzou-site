from __future__ import annotations
from pydantic import BaseModel, BaseConfig, HttpUrl, validator
from datetime import datetime, timezone
from re import match


def datetime_to_str(dt: datetime) -> str:
    return dt.replace(tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z')


class Model(BaseModel):
    class Config(BaseConfig):
        json_encoders = {datetime: datetime_to_str}


class Schema(BaseModel):
    class Config(BaseModel.Config):
        orm_mode: bool = True


class Article(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    tags: list[str]
    author: str = 'Daniel Zou'
    time_created: datetime
    time_updated: datetime
    views: int

    @validator('tags', each_item=True)
    def check_tags(cls, value: str) -> str:
        if match(r'^[\w]+([-\.][\w]+)*$', value):
            return value
        raise ValueError('invalid tag format')

    @validator('time_created', 'time_updated')
    def default_datetime(cls, value: datetime) -> datetime:
        value or datetime.now()


class ShortURL(BaseModel):
    from_id: HttpUrl
    redirect_url: HttpUrl
