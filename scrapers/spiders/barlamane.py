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
            # barlamane.com uses encoded Arabic slugs without numeric segments
            if ("barlamane.com/" in href
                    and href not in (self.base_url + "/", "https://barlamane.com/")
                    and "/category/" not in href
                    and "/tag/" not in href
                    and "/page/" not in href
                    and "/fr/" not in href
                    and "barlamaneradio" not in href
                    and "barlamanesport" not in href
                    and "wadifa" not in href):
                # Only article slugs (contain encoded Arabic or long paths)
                path = href.split("barlamane.com/")[-1].strip("/")
                if path and "%" in path:
                    full = href if href.startswith("http") else "https://barlamane.com/" + path
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
