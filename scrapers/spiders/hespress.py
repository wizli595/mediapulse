from __future__ import annotations

from datetime import datetime

from scrapers.base import AbstractSpider
from scrapers.fetcher import fetch_and_parse
from shared.exceptions import ScrapingError
from shared.logging import get_logger
from shared.models import Article

_log = get_logger(__name__)


class HespressSpider(AbstractSpider):

    @property
    def name(self) -> str:
        return "hespress"

    @property
    def base_url(self) -> str:
        return "https://www.hespress.com"

    def get_article_urls(self) -> list[str]:
        soup = fetch_and_parse(self.base_url)
        urls: set[str] = set()

        for card in soup.select("div.overlay.card a.stretched-link"):
            href = card.get("href", "")
            if href.endswith(".html"):
                urls.add(href)

        for link in soup.select("#headlinesCarousel .carousel-item h3 a"):
            href = link.get("href", "")
            if href.endswith(".html"):
                urls.add(href)

        _log.info("Found %d article URLs on %s", len(urls), self.name)
        return list(urls)

    def parse_article(self, url: str) -> Article | None:
        try:
            soup = fetch_and_parse(url)
        except ScrapingError:
            _log.warning("Failed to fetch %s", url)
            return None

        title = self._text(soup, "h1.post-title")
        if not title:
            return None

        content = "\n".join(
            p.get_text(strip=True)
            for p in soup.select("div.article-content p")
            if p.get_text(strip=True)
        )

        ld = self._extract_jsonld(soup)
        published_at = self._parse_date(ld.get("datePublished")) if ld else None

        breadcrumbs = soup.select("nav.post_breadcrumb .breadcrumb-item a")
        category = breadcrumbs[-1].get_text(strip=True) if len(breadcrumbs) > 1 else None

        return Article(
            title=title,
            content=content,
            source=self.name,
            url=url,
            published_at=published_at or datetime.utcnow(),
            author=self._text(soup, "span.author a"),
            category=category,
        )
