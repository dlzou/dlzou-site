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


class Model(BaseModel):
    class Config:
        json_encoders = {datetime: datetime_to_str}


class BaseArticle(Model):
    title: str
    author = 'Daniel Zou'
    description: str


class CreateArticle(BaseArticle):
    body: str
    tags: list[str]

    _check_tags = validator('tags', each_item=True, allow_reuse=True)(check_tag)


class UpdateArticle(BaseArticle):
    id_: str
    body: str
    tags: list[str]

    _check_tags = validator('tags', each_item=True, allow_reuse=True)(check_tag)


class Article(BaseArticle):
    id_: str
    body: str
    time_created: datetime
    time_updated: Optional[datetime] = None
    views: int
    tags: list[Tag]

    class Config(Model.Config):
        orm_mode = True


class Preview(BaseArticle):
    id_: str
    time_created: datetime
    time_updated: Optional[datetime] = None
    tags: list[Tag]

    class Config(Model.Config):
        orm_mode = True


class PreviewList(Model):
    previews: list[Preview]
    filter_tags: list[Tag] = []


class Tag(BaseModel):
    id_: str
    label: str
    count: int

    class Config:
        orm_mode = True
