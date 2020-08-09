from sqlalchemy.orm import Session

from app.db.models import Admin


def authenticate(db: Session, username: str):
    admin = db.query(Admin).filter(Admin.username == username).first()
    return admin
