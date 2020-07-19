from __future__ import annotations
from pydantic import BaseModel, BaseConfig, HttpUrl, validator
from datetime import datetime, timezone
from re import match


def datetime_to_str(dt: datetime) -> str:
    return dt.replace(tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z')


class Model(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name = True
        json_encoders = {datetime: datetime_to_str}


class Schema(Model):
    class Config(BaseModel.Config):
        orm_mode = True 


class Article(Model):
    slug: str
    chron_id: int
    title: str
    description: str
    body: str
    tags: list[str]
    author = 'Daniel Zou'
    time_posted: datetime
    time_updated: datetime
    views: int

    @validator('tags', each_item=True)
    def check_tag(cls, value: str) -> str:
        if match(r'^[\w]+([-\.][\w]+)*$', value):
            return value
        raise ValueError('invalid tag format')

    @validator('time_created', 'time_updated')
    def default_datetime(cls, value: datetime) -> datetime:
        value or datetime.now()


class Preview(Article):
    body = ''


class Subscriber(Model):
    email: str
    name: str

    @validator('email')
    def check_email(cls, value: str) -> str:
        if match(r'^[^@\s]+@\w+(-\w+)*(\.\w+(-\w+)*){1,3}$', value):
            return value
        raise ValueError('invalid email format')


class ShortURL(Model):
    from_id: HttpUrl
    redirect_url: HttpUrl
