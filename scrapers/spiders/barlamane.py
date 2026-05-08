from __future__ import annotations

from datetime import datetime

from scrapers.base import AbstractSpider
from scrapers.fetcher import fetch_and_parse
from shared.exceptions import ScrapingError
from shared.logging import get_logger
from shared.models import Article

_log = get_logger(__name__)


class BarlamaneSpider(AbstractSpider):

    @property
    def name(self) -> str:
        return "barlamane"

    @property
    def base_url(self) -> str:
        return "https://www.barlamane.com"

    def get_article_urls(self) -> list[str]:
        soup = fetch_and_parse(self.base_url)
        urls: set[str] = set()

        for link in soup.select("a[href]"):
            href = link.get("href", "")
            if self.base_url in href and href != self.base_url + "/":
                if any(seg.isdigit() for seg in href.rstrip("/").split("/")):
                    urls.add(href)

        _log.info("Found %d article URLs on %s", len(urls), self.name)
        return list(urls)

    def parse_article(self, url: str) -> Article | None:
        try:
            soup = fetch_and_parse(url)
        except ScrapingError:
            _log.warning("Failed to fetch %s", url)
            return None

        title = self._text(soup, "h1")
        if not title:
            return None

        content = "\n".join(
            p.get_text(strip=True)
            for p in soup.select("article p, .entry-content p, .post-content p")
            if p.get_text(strip=True)
        )

        ld = self._extract_jsonld(soup)
        published_at = self._parse_date(ld.get("datePublished")) if ld else None

        return Article(
            title=title,
            content=content,
            source=self.name,
            url=url,
            published_at=published_at or datetime.utcnow(),
            author=self._text(soup, ".author a, .post-author"),
            category=self._text(soup, ".category a, .breadcrumb a:last-child"),
        )
