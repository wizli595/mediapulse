from __future__ import annotations

from dataclasses import replace

from ingestion.serializers.article import article_to_bytes
from processing.silver.deduplicator import is_duplicate
from processing.silver.html_cleaner import strip_html
from processing.silver.language_detector import detect_language
from processing.silver.text_normalizer import normalize_text
from shared.logging import get_logger
from shared.models import Article
from storage.base import AbstractStorage

_log = get_logger(__name__)


def process_to_silver(article: Article, storage: AbstractStorage) -> Article | None:
    """Run all silver transformations on one article.

    Returns the cleaned Article, or None if it's a duplicate.
    """
    if is_duplicate(article, storage):
        _log.info("Silver: skipping duplicate %s", article.article_id)
        return None

    cleaned_content = strip_html(article.content)
    normalized_content = normalize_text(cleaned_content)
    language = detect_language(normalized_content)

    cleaned = replace(
        article,
        content=normalized_content,
        language=language,
    )

    date_prefix = cleaned.published_at.strftime("%Y/%m/%d")
    key = f"{cleaned.source}/{date_prefix}/{cleaned.article_id}.json"
    storage.write("silver", key, article_to_bytes(cleaned))
    _log.info("Silver: wrote %s (lang=%s)", key, language)

    return cleaned
