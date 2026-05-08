from __future__ import annotations

from datetime import datetime

from scrapers.base import AbstractSpider
from scrapers.fetcher import fetch_and_parse
from shared.exceptions import ScrapingError
from shared.logging import get_logger
from shared.models import Article

_log = get_logger(__name__)


class AlJazeeraSpider(AbstractSpider):

    @property
    def name(self) -> str:
        return "aljazeera"

    @property
    def base_url(self) -> str:
        return "https://www.aljazeera.com"

    def get_article_urls(self) -> list[str]:
        soup = fetch_and_parse(self.base_url)
        urls: set[str] = set()

        prefixes = ("/news/", "/features/", "/opinion/", "/economy/")
        for link in soup.select("a[href]"):
            href = link.get("href", "")
            if any(href.startswith(p) for p in prefixes):
                urls.add(self.base_url + href)

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

        main = soup.select_one("main") or soup
        content = "\n".join(
            p.get_text(strip=True)
            for p in main.select("p")
            if p.get_text(strip=True)
        )

        ld = self._extract_jsonld(soup)
        published_at = self._parse_date(ld.get("datePublished")) if ld else None

        author_el = soup.select_one('a[href^="/author/"]')
        author = author_el.get_text(strip=True) if author_el else None

        category = url.split("/")[3] if len(url.split("/")) > 3 else None

        return Article(
            title=title,
            content=content,
            source=self.name,
            url=url,
            published_at=published_at or datetime.utcnow(),
            author=author,
            category=category,
        )
