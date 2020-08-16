from typing import Optional
from jose import jwt
from passlib.context import CryptoContext
from datetime import datetime, timedelta
from pydantic import ValidationError

from app.core import config
from app.schemas import TokenPayload


def create_access_token(subject: str) -> str:
    expires_delta = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MIN)
    ...


def decode_token(token: str) -> Optional[TokenPayload]:
    """
    Return decoded subject for valid tokens, or None for expired tokens.
    """
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=['HS256'])
        return TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        return None


def check_password(password: str, password_hash: str) -> bool:
    ...
