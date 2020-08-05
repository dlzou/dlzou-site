from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, not_
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timezone

from app.schemas import CreateArticle, UpdateArticle, Preview, PreviewList
from app.db.models import Article, Tag, ArticleToTag


def get_article_by_id(db: Session, article_id: str) -> Article:
    article = db.query(Article).filter(Article.id_ == article_id).first()
    return article


def get_ids_by_filters(db: Session,
                       tags: list[str],
                       years: list[int],
                       limits: tuple[int, int]
                       ) -> list[int]:
    tags[:] = _process_tag_labels(db, tags, create=False)
    article_ids = db.query(Article.id_)

    if len(tags) > 0:
        article_ids = article_ids.filter(Article.tags.any(Tag.label.in_(tags)))

    if len(years) > 0:
        article_ids = article_ids.filter(Article.time_created.year.in_(years))

    article_ids = article_ids.all()[limits[0]:limits[1]]
    return article_ids


def get_preview_by_id(db: Session, article_id: int) -> Preview:
    article = db.query(Article).filter(Article.id_ == article_id).first()
    return Preview.from_orm(article)


def create_article(db: Session, obj_in: CreateArticle) -> Article:
    json_in = jsonable_encoder(obj_in)
    meta = {
        'id_': _new_article_id(db),
        'time_created': datetime.now(timezone.utc),
        'views': 0,
        'tags': _process_tag_labels(json_in.tags, create=True)
    }
    json_in.pop('tags')
    article = Article(**json_in, **meta)
    db.add(article)
    db.commit()
    return article


def update_article(db: Session, obj_in: UpdateArticle) -> Article:
    json_in = jsonable_encoder(obj_in)
    meta = {
        'time_updated': datetime.now(timezone.utc),
        'tags': _process_tag_labels(json_in.tags, create=True)
    }
    json_in.pop('tags')
    update = {**json_in, **meta}
    article = get_article_by_id(json_in['id_'])
    for attr in update:
        setattr(article, attr, update[attr])
    db.commit()
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


def _process_tag_labels(db: Session, tag_labels: list[str], create=True) -> list[Tag]:
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
