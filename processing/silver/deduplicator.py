from __future__ import annotations

from shared.models import Article
from storage.base import AbstractStorage


def is_duplicate(article: Article, storage: AbstractStorage) -> bool:
    """Check if an article already exists in the silver layer by its ID."""
    date_prefix = article.published_at.strftime("%Y/%m/%d")
    key = f"{article.source}/{date_prefix}/{article.article_id}.json"
    return storage.exists("silver", key)
