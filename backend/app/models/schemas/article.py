from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field

from ..domains import Article


class ArticleInResponse(Article):
    tags: list[str]
