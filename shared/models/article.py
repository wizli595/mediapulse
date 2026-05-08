from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class Article:
    """Single news article — the core domain model used by every layer."""

    title: str
    content: str
    source: str
    url: str
    published_at: datetime
    scraped_at: datetime = field(default_factory=_utcnow)
    author: str | None = None
    category: str | None = None
    language: str | None = None

    @property
    def article_id(self) -> str:
        """Deterministic ID derived from source + URL. Stable across runs."""
        from hashlib import sha256

        raw = f"{self.source}:{self.url}"
        return sha256(raw.encode()).hexdigest()[:16]
