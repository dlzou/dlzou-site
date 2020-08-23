from typing import Optional
from jose import jwt
from passlib.context import CryptoContext
from datetime import datetime, timedelta
from pydantic import ValidationError

from app.core import config
from app.schemas import TokenPayload


pwd_context = CryptoContext(schemes=['bcrypt'], deprecated='auto')


def create_access_token(data: dict, delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if delta:
        expires = datetime.utcnow() + delta
    else:
        expires = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MIN)
    to_encode.update({'exp': expires})
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.JWT_SIGN_ALGORITHM)


def decode_token(token: str) -> Optional[TokenPayload]:
    """
    Return decoded subject for valid tokens, or None for expired tokens.
    """
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.JWT_SIGN_ALGORITHM])
        return TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        return None


def check_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def get_password_hash(password):
    return pwd_context.hash(password)
