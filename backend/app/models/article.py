from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, validator
from datetime import datetime, timezone
from re import match


def datetime_to_str(dt: datetime) -> str:
    return dt.replace(tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z')


def check_tag(cls, value: str) -> str:
    if len(value) <= 30 and match(r'^[\w]+([-\.][\w]+)*$', value):
        return value
    raise ValueError('invalid tag format')


def default_datetime(cls, value: datetime) -> datetime:
    value or datetime.now()


class Model(BaseModel):
    class Config:
        json_encoders = {datetime: datetime_to_str}


class BaseArticle(Model):
    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None
    author: str = 'Daniel Zou'


class Preview(BaseArticle):
    id_: str
    slug: str
    title: str
    description: str
    time_created: datetime
    time_updated: Optional[datetime] = None
    views: int
    tags: list[Tag]


class PreviewList(Model):
    previews: list[Preview]


class CreateArticle(BaseArticle):
    title: str
    description: str
    body: str
    time_created: datetime
    tags: list[str]

    _check_tags = validator('tags', each_item=True, allow_reuse=True)(check_tag)

    _default_datetime = validator('time_created', allow_reuse=True)(default_datetime)


class UpdateArticle(BaseArticle):
    id_: str
    title: str
    description: str
    body: str
    time_updated: datetime
    tags: list[str]

    _check_tags = validator('tags', each_item=True, allow_reuse=True)(check_tag)

    _default_datetime = validator('time_updated', allow_reuse=True)(default_datetime)


class ArticleInDB(BaseArticle):
    id_: str
    slug: str
    title: str
    description: str
    body: str
    author: str
    time_posted: datetime
    time_updated: datetime
    views: int
    tags: list[Tag]

    class Config(Model.Config):
        orm_mode = True


class Tag(BaseModel):
    id_: str
    label: str
    count: int

    _check_tag = validator('label', allow_reuse=True)(check_tag)

    class Config:
        orm_mode = True
