from typing import Optional
from sqlalchemy.orm import Session

from app.db.models import Admin
from app.core import security


def get_by_email(db: Session, email: str) -> Optional[Admin]:
    return db.query(Admin).filter(Admin.email == email).first()


def authenticate(db: Session, email: str, password: str) -> Optional[Admin]:
    admin = get_by_email(db, email)
    if not admin:
        return None
    if not security.check_password(password, admin.password_hash):
        return None
    return admin
