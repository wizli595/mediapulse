from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from shared.models import Article


@dataclass(frozen=True)
class SourceCount:
    source: str
    article_count: int


def count_by_source(articles: list[Article]) -> list[SourceCount]:
    """Count total articles per source."""
    counts = Counter(a.source for a in articles)
    return [
        SourceCount(source=source, article_count=count)
        for source, count in counts.most_common()
    ]
