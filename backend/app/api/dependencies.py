from __future__ import annotations
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.orm import Session
from re import sub

from app.core import config, security
from app.db.session import SessionFactory


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{config.API_PATH}/login/access-token')


def get_db() -> Generator:
    try:
        db = SessionFactory()
        yield db
    finally:
        db.close()


def is_admin(token: str = Depends(oauth2_scheme)) -> bool:
    """
    Global authentication.

    Only one session can exist at any time, and the token expires after one hour of inactivity.
    New login invalidates the previous token.
    """
    ...


def get_slug(title: str) -> str:
    words = sub(r'[^\sa-z0-9]+', '', title.lower()).split()
    return '-'.join(words)
