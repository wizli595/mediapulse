from __future__ import annotations

import json

from processing.gold.source_counter import SourceCount, count_by_source
from processing.gold.topic_extractor import TopicRecord, extract_topics
from processing.gold.trend_aggregator import TrendRecord, compute_trends
from shared.logging import get_logger
from shared.models import Article
from storage.base import AbstractStorage

_log = get_logger(__name__)


def _serialize_trends(records: list[TrendRecord]) -> bytes:
    data = [
        {"date": r.date, "source": r.source, "category": r.category, "article_count": r.article_count}
        for r in records
    ]
    return json.dumps(data, ensure_ascii=False).encode("utf-8")


def _serialize_topics(records: list[TopicRecord]) -> bytes:
    data = [{"keyword": r.keyword, "frequency": r.frequency} for r in records]
    return json.dumps(data, ensure_ascii=False).encode("utf-8")


def _serialize_sources(records: list[SourceCount]) -> bytes:
    data = [{"source": r.source, "article_count": r.article_count} for r in records]
    return json.dumps(data, ensure_ascii=False).encode("utf-8")


def process_to_gold(articles: list[Article], storage: AbstractStorage) -> None:
    """Run all gold aggregations and write results to the gold layer."""
    if not articles:
        _log.info("Gold: no articles to process")
        return

    trends = compute_trends(articles)
    storage.write("gold", "trends.json", _serialize_trends(trends))
    _log.info("Gold: wrote trends.json (%d records)", len(trends))

    topics = extract_topics(articles)
    storage.write("gold", "topics.json", _serialize_topics(topics))
    _log.info("Gold: wrote topics.json (%d keywords)", len(topics))

    sources = count_by_source(articles)
    storage.write("gold", "sources.json", _serialize_sources(sources))
    _log.info("Gold: wrote sources.json (%d sources)", len(sources))
