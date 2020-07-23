from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, not_
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timezone

from app.schemas.article import CreateArticle, UpdateArticle, Preview, PreviewList
from app.db.models import Article, Tag, ArticleToTag


def get_article_by_id(db: Session, article_id: str) -> Article:
    article = db.query(Article).filter(Article.id_ == article_id).first()
    return article


# assume all tags exist
def get_articles_by_filters(db: Session, tags: list[str], years: list[str]) -> list[str]:
    pass


def get_preview_by_id(db: Session, article_id: str) -> Preview:
    article = db.query(Article).filter(Article.id_ == article_id).first()
    return Preview.from_orm(article)


def create_article(db: Session, obj_in: CreateArticle) -> Article:
    json_in = jsonable_encoder(obj_in)
    meta = {
        'id_': _new_article_id(db),
        'time_created': datetime.now(timezone.utc),
        'views': 0,
        'tags': _process_str_tags(json_in.tags, create=True)
    }
    json_in.pop('tags')
    article = Article(**json_in, **meta)
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


def update_article(db: Session, obj_in: UpdateArticle) -> Article:
    json_in = jsonable_encoder(obj_in)
    meta = {
        'time_updated': datetime.now(timezone.utc),
        'tags': _process_str_tags(json_in.tags, create=True)
    }
    json_in.pop('tags')
    update = {**json_in, **meta}
    article = get_article_by_id(json_in['id_'])
    for attr in update:
        setattr(article, attr, update[attr])
    db.commit()
    db.refresh(article)
    return article


def delete_article(db: Session, id_: int) -> Article:
    article = db.query(Article).get(id_)
    db.delete(article)
    db.commit()
    return article


def _new_article_id(db: Session) -> int:
    max = db.query(func.max(Article.id_)).scalar()
    return 0 if max is None else max + 1


def _new_tag_id(db: Session) -> int:
    max = db.query(func.max(Tag.id_)).scalar()
    return 0 if max is None else max + 1


def _process_str_tags(str_tags: list[str], create=True) -> list[Tag]:
    ...
