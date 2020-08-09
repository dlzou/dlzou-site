from jose import jwt
from passlib.context import CryptoContext

from app.core import config


def create_access_token() -> str:
    ...


def check_password(password: str, password_hash: str) -> bool:
    ...
