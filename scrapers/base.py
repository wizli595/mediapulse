from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime

from bs4 import BeautifulSoup

from shared.models import Article


class AbstractSpider(ABC):
    """Contract that every spider must follow.

    A spider does exactly two things:
      1. Discover article URLs from a source.
      2. Parse a single URL into an Article.

    It does NOT publish, store, validate, or transform.
    Shared helpers live here so spiders stay DRY.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for this source (e.g. 'hespress')."""

    @property
    @abstractmethod
    def base_url(self) -> str:
        """Root URL of the news source."""

    @abstractmethod
    def get_article_urls(self) -> list[str]:
        """Return a list of article URLs to scrape."""

    @abstractmethod
    def parse_article(self, url: str) -> Article | None:
        """Parse a single URL into an Article. Return None if parsing fails."""

    # -- Shared helpers (used by multiple spiders) --

    def _text(self, soup: BeautifulSoup, selector: str) -> str | None:
        """Extract stripped text from the first element matching a CSS selector."""
        el = soup.select_one(selector)
        return el.get_text(strip=True) if el else None

    def _extract_jsonld(self, soup: BeautifulSoup, target_type: str = "NewsArticle") -> dict | None:
        """Extract JSON-LD block matching a given @type."""
        for script in soup.select('script[type="application/ld+json"]'):
            try:
                data = json.loads(script.string)
                if data.get("@type") == target_type:
                    return data
            except (json.JSONDecodeError, TypeError):
                continue
        return None

    def _parse_date(self, date_str: str | None) -> datetime | None:
        """Parse an ISO-format date string. Returns None on failure."""
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str)
        except ValueError:
            return None
