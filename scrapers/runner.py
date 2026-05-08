from __future__ import annotations

from scrapers.base import AbstractSpider
from scrapers.registry import get_all_spiders
from shared.logging import get_logger
from shared.models import Article

_log = get_logger(__name__)


def run_spider(spider: AbstractSpider) -> list[Article]:
    """Run a single spider: discover URLs, parse each one, return articles."""
    _log.info("Starting spider: %s", spider.name)

    urls = spider.get_article_urls()
    articles: list[Article] = []

    for url in urls:
        article = spider.parse_article(url)
        if article:
            articles.append(article)

    _log.info("Spider %s finished: %d articles collected", spider.name, len(articles))
    return articles


def run_all_spiders() -> list[Article]:
    """Run every registered spider and return all articles."""
    all_articles: list[Article] = []

    for spider in get_all_spiders():
        try:
            articles = run_spider(spider)
            all_articles.extend(articles)
        except Exception:
            _log.exception("Spider %s crashed", spider.name)

    _log.info("All spiders finished: %d total articles", len(all_articles))
    return all_articles
