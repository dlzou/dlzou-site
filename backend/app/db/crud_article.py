from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy.sql import not_

from app.models.article import Article, CreateArticle, UpdateArticle, Preview, PreviewList
from app.db.schemas import Article as ArticleTbl, Tag as TagTbl, ArticleToTag as AssocTbl


def get_article_by_id(db: Session, article_id: str) -> Article:
    article_rec = db.query(ArticleTbl).filter(ArticleTbl.id_ == article_id).first()
    return Article.from_orm(article_rec)


def get_article_ids_by_tags(db: Session, tags: list[str]) -> list[str]:
    pass


def get_preview_by_id(db: Session, article_id: str) -> Preview:
    article_rec = db.query(ArticleTbl).filter(ArticleTbl.id_ == article_id).first()
    return Preview.from_orm(article_rec)
