from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, validator
from datetime import datetime, timezone
from re import match


def datetime_to_str(dt: datetime) -> str:
    return dt.replace(tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z')


def check_tag(cls, value: str) -> str:
    if match(r'^[\w]+([-\.][\w]+)*$', value):
        return value
    raise ValueError('invalid tag format')


def default_datetime(cls, value: datetime) -> datetime:
    value or datetime.now()


class Model(BaseModel):
    class Config:
        allow_population_by_field_name = True
        json_encoders = {datetime: datetime_to_str}


class BaseArticle(Model):
    article_id: Optional[int] = None
    slug: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None
    tags: Optional[list[str]] = None
    author: str = 'Daniel Zou'
    time_created: Optional[datetime] = None
    time_updated: Optional[datetime] = None
    views: Optional[int] = None


class Preview(BaseArticle):
    article_id: int
    slug: int
    title: str
    description: str
    tags: list[str]
    time_created: datetime
    time_updated: Optional[datetime] = None
    views: int

    _check_tags = validator('tags', each_item=True, allow_reuse=True)(check_tag)

    _default_datetime = validator(
        'time_created', 'time_updated', allow_reuse=True)(default_datetime)


class CreateArticle(BaseArticle):
    title: str
    description: str
    body: str
    tags: list[str]
    time_created: datetime

    _check_tags = validator('tags', each_item=True, allow_reuse=True)(check_tag)

    _default_datetime = validator('time_created', allow_reuse=True)(default_datetime)


class UpdateArticle(BaseArticle):
    title: str
    description: str
    body: str
    tags: list[str]
    time_updated: datetime

    _check_tags = validator('tags', each_item=True, allow_reuse=True)(check_tag)

    _default_datetime = validator('time_updated', allow_reuse=True)(default_datetime)


class DBToArticle(BaseArticle):
    article_id: int
    slug: str
    title: str
    description: str
    body: str
    tags: list[str]
    author = 'Daniel Zou'
    time_posted: datetime
    time_updated: datetime
    views: int

    class Config(Model.Config):
        orm_mode = True
