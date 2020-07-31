from __future__ import annotations
from fastapi import APIRouter
from sqlalchemy.orm import Session

from app import schemas
from app.db import crud, models


router = APIRouter()


@router.get('/{id}', response_model=schemas.Article)
def get_article():
    ...
