from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.db import crud, models
from app.api import dependencies as dep


router = APIRouter()


@router.post('/new')
def create_article(obj_in: schemas.CreateArticle,
                   is_admin: bool = Depends(dep.authenticate),
                   db: Session = Depends(dep.get_db)):
    if not is_admin:
        raise HTTPException(status_code=400, detail='Access denied.')
    article = crud.article.create_article(db, obj_in)
    return article


@router.get('/', response_model=schemas.PreviewList)
def get_articles(db: Session = Depends(dep.get_db)):
    ...


@router.get('/{id_}', response_model=schemas.Article)
def get_article(id_: int,
                db: Session = Depends(dep.get_db)):
    article = crud.article.get_article_by_id(id_)
    if not article:
        raise HTTPException(status_code=404, detail='Article not found.')
    return article


@router.put('/{id_}', response_model=schemas.Article)
def update_article(id_: int,
                   obj_in: schemas.UpdateArticle,
                   is_admin: bool = Depends(dep.authenticate),
                   db: Session = Depends(dep.get_db)):
    if not is_admin:
        raise HTTPException(status_code=400, detail='Access denied.')
    ...


@router.delete('/{id_}', response_model=schemas.Article)
def delete_article(id_: int,
                   is_admin: bool = Depends(dep.authenticate)):
    if not is_admin:
        raise HTTPException(status_code=400, detail='Access denied.')
    ...
