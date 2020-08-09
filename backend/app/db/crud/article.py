from __future__ import annotations
from typing import Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, not_
from datetime import datetime, timezone

from app.schemas import CreateArticle, UpdateArticle, Preview, PreviewList
from app.db.models import Article, Tag, ArticleToTag


def get_article_by_id(db: Session, article_id: str) -> Optional[Article]:
    return db.query(Article).filter(Article.id_ == article_id).first()


def get_preview_by_id(db: Session, article_id: int) -> Optional[Preview]:
    article = db.query(Article).filter(Article.id_ == article_id).first()
    return Preview.from_orm(article)


def get_ids_by_filters(db: Session,
                       *,
                       tags: Union[list[str], list[Tag]] = [],
                       years: list[int] = [],
                       skip: int = 0,
                       limit: int = 10
                       ) -> list[int]:
    article_ids = db.query(Article.id_)

    if len(tags) > 0:
        if isinstance(tags[0], str):
            article_ids = article_ids.filter(Article.tags.any(Tag.label.in_(tags)))
        else:
            article_ids = article_ids.filter(Article.tags.any(Tag.in_(tags)))

    if len(years) > 0:
        article_ids = article_ids.filter(Article.time_created.year.in_(years))

    article_ids = article_ids.all()[skip: skip + limit]
    return article_ids


def create_article(db: Session, obj_in: CreateArticle) -> Article:
    meta = {
        'id_': _new_article_id(db),
        'time_created': datetime.now(timezone.utc),
        'views': 0,
        'tags': process_tag_labels(obj_in.tags, create=True)
    }
    article = Article(**obj_in.dict(exclude={'tags'}), **meta)
    db.add(article)
    db.commit()
    return article


def update_article(db: Session, obj_in: UpdateArticle) -> Optional[Article]:
    article = get_article_by_id(db, obj_in.id_)
    if article is None:
        return None

    meta = {
        'time_updated': datetime.now(timezone.utc),
        'tags': process_tag_labels(obj_in.tags, create=True)
    }
    update = {**obj_in.dict(exclude={'tags'}), **meta}
    for attr in update:
        setattr(article, attr, update[attr])
    db.commit()
    return article


def delete_article(db: Session, id_: int) -> Optional[Article]:
    article = get_article_by_id(db, id_)
    if article is None:
        return None

    db.delete(article)
    db.commit()
    return article


def _new_article_id(db: Session) -> int:
    max_id = db.query(func.max(Article.id_)).scalar()
    return 0 if max_id is None else max_id + 1


def _new_tag_id(db: Session) -> int:
    max_id = db.query(func.max(Tag.id_)).scalar()
    return 0 if max_id is None else max_id + 1


def process_tag_labels(db: Session, tag_labels: list[str], create=True) -> list[Tag]:
    '''
    Converts tag labels to SQLAlchemy objects, creating them if necessary.
    '''
    tag_labels[:] = [label.lower() for label in tag_labels]
    tags = []

    for label in tag_labels:
        tag = db.query(Tag).filter_by(label=label).one_or_none()
        if tag is None and create:
            tag = Tag(id_=_new_tag_id(db), label=label)
            db.add(tag)
            db.commit()
        if tag is not None:
            tags.append(tag)
    return tags
