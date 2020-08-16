from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.db import crud, models
from app.api import dependencies as dep


router = APIRouter()


@router.post('/new')
def create_article(obj_in: schemas.CreateArticle,
                   is_admin: bool = Depends(dep.is_admin),
                   db: Session = Depends(dep.get_db)):
    if not is_admin:
        raise HTTPException(status_code=401, detail='Access denied.')
    article = crud.article.create_article(db, obj_in)
    return article


@router.get('/', response_model=schemas.PreviewList)
def get_previews(tags: list[schemas.Tag] = [],
                 years: list[int] = [],
                 skip: int = 0,
                 limit: int = 10,
                 db: Session = Depends(dep.get_db)):
    article_ids = crud.article.get_ids_by_filters(db, tags=tags, years=years,
                                                  skip=skip, limit=limit)

    previews = [crud.get_preview_by_id(db, aid) for aid in article_ids]
    response = schemas.PreviewList(previews=previews, tags=tags, years=years,
                                   skip=skip, limit=limit)
    return response


@router.get('/{aid}', response_model=schemas.Article)
def get_article(aid: int,
                db: Session = Depends(dep.get_db)):
    article = crud.article.get_article_by_id(db, aid)
    if not article:
        raise HTTPException(status_code=404, detail='Article not found.')
    return article


@router.put('/{aid}', response_model=schemas.Article)
def update_article(aid: int,
                   obj_in: schemas.UpdateArticle,
                   is_admin: bool = Depends(dep.is_admin),
                   db: Session = Depends(dep.get_db)):
    if not is_admin:
        raise HTTPException(status_code=401, detail='Access denied.')
    if aid != obj_in.id_:
        raise HTTPException(status_code=400, detail='Bad request: article ID does not match.')

    article = crud.article.update_article(db, obj_in)
    if article is None:
        raise HTTPException(status_code=400, detail='Bad request: article does not exist.')
    return article


@router.delete('/{aid}', response_model=schemas.Article)
def delete_article(aid: int,
                   is_admin: bool = Depends(dep.is_admin),
                   db: Session = Depends(dep.get_db)):
    if not is_admin:
        raise HTTPException(status_code=401, detail='Access denied.')

    article = crud.article.remove(db, aid)
    if article is None:
        raise HTTPException(status_code=400, detail='Bad request: article does not exist.')
    return article
