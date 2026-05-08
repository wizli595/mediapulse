from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from shared.models import Article


@dataclass(frozen=True)
class TrendRecord:
    date: str
    source: str
    category: str | None
    article_count: int


def compute_trends(articles: list[Article]) -> list[TrendRecord]:
    """Aggregate articles by date + source + category."""
    counts: Counter[tuple[str, str, str | None]] = Counter()

    for a in articles:
        date_key = a.published_at.strftime("%Y-%m-%d")
        counts[(date_key, a.source, a.category)] += 1

    return [
        TrendRecord(date=date, source=source, category=cat, article_count=count)
        for (date, source, cat), count in counts.most_common()
    ]
