from __future__ import annotations
from pydantic import BaseModel, BaseConfig, validator
from datetime import datetime


class Article(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    tags: list[str]
    author: str = 'Daniel Zou'
    time_created: datetime
    time_updated: datetime

    @validator('*')
    def default_datetime(cls, value: datetime) -> datetime:
        value or datetime.now()


class ShortURL(BaseModel):
    from_id: str
    redirect_url: str
