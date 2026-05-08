from __future__ import annotations

import json
from datetime import datetime

from shared.models import Article


def article_to_json(article: Article) -> str:
    """Serialize an Article to a JSON string."""
    return json.dumps(
        {
            "title": article.title,
            "content": article.content,
            "source": article.source,
            "url": article.url,
            "published_at": article.published_at.isoformat(),
            "scraped_at": article.scraped_at.isoformat(),
            "author": article.author,
            "category": article.category,
            "language": article.language,
        },
        ensure_ascii=False,
    )


def json_to_article(raw: str) -> Article:
    """Deserialize a JSON string back into an Article."""
    data = json.loads(raw)
    return Article(
        title=data["title"],
        content=data["content"],
        source=data["source"],
        url=data["url"],
        published_at=datetime.fromisoformat(data["published_at"]),
        scraped_at=datetime.fromisoformat(data["scraped_at"]),
        author=data.get("author"),
        category=data.get("category"),
        language=data.get("language"),
    )


def article_to_bytes(article: Article) -> bytes:
    """Serialize an Article to UTF-8 bytes (for Kafka)."""
    return article_to_json(article).encode("utf-8")


def bytes_to_article(raw: bytes) -> Article:
    """Deserialize UTF-8 bytes back into an Article."""
    return json_to_article(raw.decode("utf-8"))
