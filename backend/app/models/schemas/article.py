from __future__ import annotations
from typing import Optional

from app.models.domain import Schema, Article, Preview


class RespondArticle(Schema):
    article: Article


class RespondPreviewList(Schema):
    previews: list[Preview]
    count: int


class CreateArticle(Schema):
    title: str
    description: str
    body: str
    tags: list[str] = []


class UpdateArticle(Schema):
    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None
    tags: Optional[list[str]] = None
