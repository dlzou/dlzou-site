from __future__ import annotations
from typing import Generator
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.orm import Session
from re import sub, match

from app.core import config, security
from app.db import crud
from app.db.session import SessionFactory


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{config.API_PATH}/login/access-token')


def get_db() -> Generator:
    try:
        db = SessionFactory()
        yield db
    finally:
        db.close()


def is_admin(token: str = Depends(oauth2_scheme),
             db: Session = Depends(get_db)) -> bool:
    """
    Global authentication.

    Only one session can exist at any time, and the token expires after one hour of inactivity.
    New login invalidates the previous token.
    """
    token_data = security.decode_token(token)
    if token_data:
        admin = crud.admin.get_by_email(db, email=token_data.subject)
        return admin is not None
    return False


def email_format(s: str) -> bool:
    return match(r'^[^@\s]+@\w+(-\w+)*(\.\w+(-\w+)*){1,3}$', s) is not None


def get_slug(title: str) -> str:
    return '-'.join(keywords(title))[:config.SLUG_LEN].strip('-')


def keywords(s: str) -> list[str]:
    art = ['a', 'an', 'the']
    words = sub(r'[^\sa-z0-9]+', '', s.lower()).split()
    return [w for w in words if w not in art]
