from __future__ import annotations

from datetime import datetime

from scrapers.base import AbstractSpider
from scrapers.fetcher import fetch_and_parse
from shared.exceptions import ScrapingError
from shared.logging import get_logger
from shared.models import Article

_log = get_logger(__name__)


class BBCSpider(AbstractSpider):

    @property
    def name(self) -> str:
        return "bbc"

    @property
    def base_url(self) -> str:
        return "https://www.bbc.com"

    def get_article_urls(self) -> list[str]:
        soup = fetch_and_parse(f"{self.base_url}/news")
        urls: set[str] = set()

        for card in soup.select('[data-testid$="-card"]'):
            link = card.select_one(
                'a[data-testid="internal-link"], a[data-testid="external-anchor"]'
            )
            if not link:
                continue
            href = link.get("href", "")
            if "/news/articles/" in href:
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

        article = soup.select_one("article")
        if not article:
            return None

        title = self._text(article, "h1")
        if not title:
            return None

        content = "\n".join(
            p.get_text(strip=True)
            for p in article.select('[data-component="text-block"] p')
            if p.get_text(strip=True)
        )

        time_el = article.select_one('[data-testid="byline"] time')
        published_at = self._parse_date(time_el.get("dateTime")) if time_el else None

        author_el = article.select_one('[data-testid="byline-contributors"] span')
        author = author_el.get_text(strip=True) if author_el else None

        tags = article.select('[data-component="tag-list-block"] a')
        category = tags[0].get_text(strip=True) if tags else None

        return Article(
            title=title,
            content=content,
            source=self.name,
            url=url,
            published_at=published_at or datetime.utcnow(),
            author=author,
            category=category,
        )
