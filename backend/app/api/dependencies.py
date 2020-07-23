from __future__ import annotations
from typing import Generator
from fastapi import Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.db.session import SessionFactory


def get_db() -> Generator:
    try:
        db = SessionFactory()
        yield db
    finally:
        db.close()


def is_admin() -> bool:
    ...


def get_slug() -> str:
    ...
