from __future__ import annotations
from pydantic import BaseModel, validator
from re import match


class Subscriber(BaseModel):
    sub_id: int
    email: str
    name: str

    @validator('email')
    def check_email(cls, value: str) -> str:
        if match(r'^[^@\s]+@\w+(-\w+)*(\.\w+(-\w+)*){1,3}$', value):
            return value
        raise ValueError('invalid email format')
