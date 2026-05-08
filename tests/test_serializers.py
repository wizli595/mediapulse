from ingestion.serializers.article import (
    article_to_bytes,
    article_to_json,
    bytes_to_article,
    json_to_article,
)


def test_json_roundtrip(sample_article):
    json_str = article_to_json(sample_article)
    restored = json_to_article(json_str)

    assert restored.title == sample_article.title
    assert restored.source == sample_article.source
    assert restored.url == sample_article.url
    assert restored.author == sample_article.author
    assert restored.category == sample_article.category
    assert restored.language == sample_article.language
    assert restored.article_id == sample_article.article_id


def test_bytes_roundtrip(sample_article):
    raw = article_to_bytes(sample_article)
    restored = bytes_to_article(raw)

    assert restored.title == sample_article.title
    assert restored.article_id == sample_article.article_id
    assert isinstance(raw, bytes)


def test_json_preserves_unicode():
    from datetime import datetime, timezone
    from shared.models import Article

    a = Article(
        title="اختبار عربي",
        content="محتوى المقال",
        source="hespress",
        url="https://hespress.com/ar",
        published_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
    )
    json_str = article_to_json(a)
    assert "اختبار" in json_str

    restored = json_to_article(json_str)
    assert restored.title == "اختبار عربي"
