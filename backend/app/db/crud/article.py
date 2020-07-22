from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy.sql import not_
from datetime import datetime

from app.models.article import Article, CreateArticle, UpdateArticle, Preview, PreviewList
from app.db.schemas import Article as ArticleTbl, Tag as TagTbl, ArticleToTag as AssocTbl


def get_article_by_id(db: Session, article_id: str) -> Article:
    article_rec = db.query(ArticleTbl).filter(ArticleTbl.id_ == article_id).first()
    return Article.from_orm(article_rec)


# assume all tags exist
def get_articles_by_filters(db: Session, tags: list[str], years: list[str]) -> list[str]:
    pass


def get_preview_by_id(db: Session, article_id: str) -> Preview:
    article_rec = db.query(ArticleTbl).filter(ArticleTbl.id_ == article_id).first()
    return Preview.from_orm(article_rec)


def create_article(db: Session, article: CreateArticle) -> Article:
    ...


def update_article(db: Session, article: UpdateArticle) -> Article:
    ...


def delete_article(db: Session, article: UpdateArticle) -> Article:
    ...
