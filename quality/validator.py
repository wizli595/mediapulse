from __future__ import annotations

from dataclasses import dataclass

from quality.checks.base import AbstractCheck, CheckResult, Status
from quality.checks.content_length import ContentLengthCheck
from quality.checks.date_present import DatePresentCheck
from quality.checks.title_present import TitlePresentCheck
from quality.checks.url_valid import UrlValidCheck
from shared.logging import get_logger
from shared.models import Article

_log = get_logger(__name__)

_ALL_CHECKS: list[AbstractCheck] = [
    TitlePresentCheck(),
    DatePresentCheck(),
    ContentLengthCheck(),
    UrlValidCheck(),
]


@dataclass(frozen=True)
class ValidationReport:
    article_id: str
    results: list[CheckResult]

    @property
    def passed(self) -> bool:
        return all(r.status == Status.PASS for r in self.results)

    @property
    def failures(self) -> list[CheckResult]:
        return [r for r in self.results if r.status == Status.FAIL]


def validate_article(article: Article) -> ValidationReport:
    """Run all quality checks against one article. Returns a report."""
    results = [check.run(article) for check in _ALL_CHECKS]
    report = ValidationReport(article_id=article.article_id, results=results)

    if report.passed:
        _log.info("Quality: %s passed all checks", article.article_id)
    else:
        failed = [f.check_name for f in report.failures]
        _log.warning("Quality: %s failed checks: %s", article.article_id, failed)

    return report
