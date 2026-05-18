from __future__ import annotations

import re
from datetime import datetime

from scrapers.base import AbstractSpider
from scrapers.fetcher import fetch_and_parse
from shared.exceptions import ScrapingError
from shared.logging import get_logger
from shared.models import Article

_log = get_logger(__name__)


class CNNSpider(AbstractSpider):

    @property
    def name(self) -> str:
        return "cnn"

    @property
    def base_url(self) -> str:
        return "https://edition.cnn.com"

    def get_article_urls(self) -> list[str]:
        soup = fetch_and_parse(self.base_url)
        urls: set[str] = set()

        for link in soup.select("a[href]"):
            href = link.get("href", "")
            # CNN dropped /index.html — now uses /YYYY/MM/DD/section/slug pattern
            if re.search(r"/\d{4}/\d{2}/\d{2}/", href):
                full = href if href.startswith("http") else self.base_url + href
                urls.add(full)

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
            for p in soup.select("article p, .article__content p")
            if p.get_text(strip=True)
        )

        ld = self._extract_jsonld(soup)
        published_at = self._parse_date(ld.get("datePublished")) if ld else None

        author = self._text(soup, ".byline__name, .metadata__byline__author")

        parts = url.split("/")
        category = parts[3] if len(parts) > 3 and not parts[3].isdigit() else None

        return Article(
            title=title,
            content=content,
            source=self.name,
            url=url,
            published_at=published_at or datetime.utcnow(),
            author=author,
            category=category,
        )
