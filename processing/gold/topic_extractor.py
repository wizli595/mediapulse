from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass

from shared.models import Article

_STOPWORDS = frozenset({
    "the", "a", "an", "is", "are", "was", "were", "in", "on", "at", "to",
    "for", "of", "and", "or", "but", "with", "by", "from", "as", "it",
    "this", "that", "which", "who", "what", "how", "not", "no", "be",
    "have", "has", "had", "do", "does", "did", "will", "would", "can",
    "could", "should", "may", "might", "shall", "its", "he", "she",
    "they", "we", "you", "i", "me", "my", "his", "her", "our", "their",
    "than", "then", "also", "just", "more", "some", "any", "all",
    "من", "في", "على", "إلى", "عن", "أن", "هذا", "هذه", "التي", "الذي",
    "بين", "بعد", "قبل", "حتى", "ما", "لا", "قد", "كان", "التي", "ذلك",
})


@dataclass(frozen=True)
class TopicRecord:
    keyword: str
    frequency: int


def extract_topics(articles: list[Article], top_n: int = 50) -> list[TopicRecord]:
    """Extract most frequent keywords across all articles."""
    word_counts: Counter[str] = Counter()

    for a in articles:
        words = re.findall(r"\b\w{3,}\b", a.content.lower())
        meaningful = [w for w in words if w not in _STOPWORDS and not w.isdigit()]
        word_counts.update(meaningful)

    return [
        TopicRecord(keyword=word, frequency=count)
        for word, count in word_counts.most_common(top_n)
    ]
