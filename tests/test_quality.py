from datetime import datetime, timezone

from quality.checks.base import Dimension, Status
from quality.checks.content_length import ContentLengthCheck
from quality.checks.date_present import DatePresentCheck
from quality.checks.title_present import TitlePresentCheck
from quality.checks.url_valid import UrlValidCheck
from quality.validator import validate_article
from shared.models import Article


def test_title_present_pass(sample_article):
    result = TitlePresentCheck().run(sample_article)
    assert result.status == Status.PASS
    assert result.dimension == Dimension.COMPLETENESS


def test_title_present_fail():
    a = Article(title="", content="x", source="s", url="https://a.com/1", published_at=datetime(2025, 1, 1, tzinfo=timezone.utc))
    result = TitlePresentCheck().run(a)
    assert result.status == Status.FAIL


def test_date_present_pass(sample_article):
    result = DatePresentCheck().run(sample_article)
    assert result.status == Status.PASS


def test_content_length_pass(sample_article):
    result = ContentLengthCheck().run(sample_article)
    assert result.status == Status.PASS


def test_content_length_fail(minimal_article):
    result = ContentLengthCheck().run(minimal_article)
    assert result.status == Status.FAIL
    assert result.dimension == Dimension.VALIDITY


def test_url_valid_pass(sample_article):
    result = UrlValidCheck().run(sample_article)
    assert result.status == Status.PASS


def test_url_valid_fail():
    a = Article(title="T", content="C", source="s", url="not-a-url", published_at=datetime(2025, 1, 1, tzinfo=timezone.utc))
    result = UrlValidCheck().run(a)
    assert result.status == Status.FAIL
    assert result.dimension == Dimension.CONSISTENCY


def test_validator_all_pass(sample_article):
    report = validate_article(sample_article)
    assert report.passed
    assert len(report.failures) == 0


def test_validator_with_failures():
    bad = Article(title="", content="short", source="s", url="bad", published_at=datetime(2025, 1, 1, tzinfo=timezone.utc))
    report = validate_article(bad)
    assert not report.passed
    assert len(report.failures) == 3  # title, content_length, url_valid
