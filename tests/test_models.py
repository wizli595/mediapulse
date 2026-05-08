from datetime import datetime, timezone

from shared.models import Article


def test_article_creation(sample_article):
    assert sample_article.title == "Test Article Title"
    assert sample_article.source == "hespress"
    assert sample_article.author == "Test Author"


def test_article_id_deterministic(sample_article):
    """Same source + URL must always produce the same ID."""
    copy = Article(
        title="Different title",
        content="Different content",
        source=sample_article.source,
        url=sample_article.url,
        published_at=datetime(2099, 1, 1, tzinfo=timezone.utc),
    )
    assert sample_article.article_id == copy.article_id


def test_article_id_differs_by_url():
    a = Article(title="T", content="C", source="s", url="https://a.com/1", published_at=datetime(2025, 1, 1, tzinfo=timezone.utc))
    b = Article(title="T", content="C", source="s", url="https://a.com/2", published_at=datetime(2025, 1, 1, tzinfo=timezone.utc))
    assert a.article_id != b.article_id


def test_article_is_frozen(sample_article):
    try:
        sample_article.title = "new"
        assert False, "Should raise FrozenInstanceError"
    except AttributeError:
        pass


def test_article_scraped_at_auto_set():
    a = Article(title="T", content="C", source="s", url="https://a.com/x", published_at=datetime(2025, 1, 1, tzinfo=timezone.utc))
    assert a.scraped_at is not None
