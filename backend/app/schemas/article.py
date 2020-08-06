from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, validator
from datetime import datetime
from re import match


def datetime_str(dt: datetime) -> str:
    return dt.isoformat()


def check_tag(cls, value: str) -> str:
    if len(value) <= 30 and match(r'^[\w]+([-\.][\w]+)*$', value):
        return value
    raise ValueError('invalid tag format')


class Model(BaseModel):
    class Config:
        json_encoders = {datetime: datetime_str}


class BaseArticle(Model):
    title: str
    author = 'Daniel Zou'
    description: Optional[str]


class CreateArticle(BaseArticle):
    body: str
    tags: list[str]

    _check_tags = validator('tags', each_item=True, allow_reuse=True)(check_tag)


class UpdateArticle(BaseArticle):
    id_: int
    body: str
    tags: list[str]

    _check_tags = validator('tags', each_item=True, allow_reuse=True)(check_tag)


class Article(BaseArticle):
    id_: int
    body: str
    time_created: datetime
    time_updated: Optional[datetime] = None
    views: int
    tags: list[Tag]

    class Config(Model.Config):
        orm_mode = True


class Preview(BaseArticle):
    id_: int
    time_created: datetime
    time_updated: Optional[datetime] = None
    tags: list[Tag]

    class Config(Model.Config):
        orm_mode = True


class PreviewList(Model):
    previews: list[Preview]
    tags: list[Tag] = []
    years: list[int] = []
    skip: int
    limit: int


class Tag(BaseModel):
    id_: int
    label: str
    count: int

    class Config:
        orm_mode = True
