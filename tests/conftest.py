from __future__ import annotations

import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pytest

from shared.models import Article
from storage.local_storage import LocalStorage


@pytest.fixture
def sample_article() -> Article:
    return Article(
        title="Test Article Title",
        content="This is a long enough test article content for validation purposes and testing.",
        source="hespress",
        url="https://www.hespress.com/test-article-123.html",
        published_at=datetime(2025, 6, 15, 12, 0, tzinfo=timezone.utc),
        author="Test Author",
        category="politics",
        language="en",
    )


@pytest.fixture
def minimal_article() -> Article:
    return Article(
        title="Minimal",
        content="Short",
        source="bbc",
        url="https://bbc.com/1",
        published_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
    )


@pytest.fixture
def article_list() -> list[Article]:
    base = datetime(2025, 6, 1, tzinfo=timezone.utc)
    return [
        Article(title="Article A", content="Content about Morocco football and sports news today.", source="hespress", url="https://hespress.com/a", published_at=base, category="sports"),
        Article(title="Article B", content="Content about Morocco football and economy growth today.", source="hespress", url="https://hespress.com/b", published_at=base, category="economy"),
        Article(title="Article C", content="Content about technology and artificial intelligence worldwide.", source="bbc", url="https://bbc.com/c", published_at=base, category="tech"),
        Article(title="Article D", content="Content about global politics and elections happening today.", source="cnn", url="https://cnn.com/d", published_at=datetime(2025, 6, 2, tzinfo=timezone.utc), category="politics"),
    ]


@pytest.fixture
def tmp_storage(tmp_path) -> LocalStorage:
    return LocalStorage(tmp_path)
