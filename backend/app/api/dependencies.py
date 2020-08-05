from __future__ import annotations
from typing import Generator
from fastapi import Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.orm import Session
from re import sub

from app.db.session import SessionFactory


def get_db() -> Generator:
    try:
        db = SessionFactory()
        yield db
    finally:
        db.close()


def authenticate(token: str) -> bool:
    ...


def get_slug(title: str) -> str:
    words = sub(r'[^\sa-z0-9]+', '', title.lower()).split()
    return '-'.join(words)
