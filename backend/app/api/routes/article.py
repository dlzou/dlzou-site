from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.db import crud, models
from app.api import dependencies as dep


router = APIRouter()


@router.post('/')
def create_article(db: Session = Depends(dep.get_db),
                   article=schemas.CreateArticle
                   ) -> schemas.Article:
    ...


@router.get('/{id_}', response_model=schemas.Article)
def get_article(db: Session = Depends(dep.get_db)):
    ...


@router.put('/{id_}')
def update_article(db: Session = Depends(dep.get_db)):
    ...
