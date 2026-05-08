from unittest.mock import patch

from scrapers.registry import get_all_spiders, get_spider_by_name


def test_registry_returns_all_spiders():
    spiders = get_all_spiders()
    assert len(spiders) == 8


def test_registry_names():
    spiders = get_all_spiders()
    names = {s.name for s in spiders}
    expected = {"hespress", "akhbarona", "lakom", "barlamane", "aljazeera", "bbc", "cnn", "reuters"}
    assert names == expected


def test_get_spider_by_name():
    spider = get_spider_by_name("bbc")
    assert spider is not None
    assert spider.name == "bbc"
    assert "bbc.com" in spider.base_url


def test_get_spider_by_name_not_found():
    assert get_spider_by_name("nonexistent") is None


def test_runner_with_mock():
    from scrapers.runner import run_spider

    spider = get_spider_by_name("hespress")

    with patch.object(spider, "get_article_urls", return_value=[]), \
         patch.object(spider, "parse_article", return_value=None):
        articles = run_spider(spider)
        assert articles == []
