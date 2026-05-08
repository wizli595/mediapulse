from __future__ import annotations

from ingestion.serializers.article import article_to_bytes
from shared.logging import get_logger
from shared.models import Article
from storage.base import AbstractStorage

_log = get_logger(__name__)


def write_raw_article(article: Article, storage: AbstractStorage) -> str:
    """Write a raw article to the bronze layer. Returns the storage key."""
    date_prefix = article.published_at.strftime("%Y/%m/%d")
    key = f"{article.source}/{date_prefix}/{article.article_id}.json"

    storage.write("bronze", key, article_to_bytes(article))
    _log.info("Bronze: wrote %s", key)
    return key
