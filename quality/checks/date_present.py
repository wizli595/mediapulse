from __future__ import annotations

from quality.checks.base import AbstractCheck, CheckResult, Dimension, Status
from shared.models import Article


class DatePresentCheck(AbstractCheck):

    @property
    def name(self) -> str:
        return "date_present"

    @property
    def dimension(self) -> Dimension:
        return Dimension.COMPLETENESS

    def run(self, article: Article) -> CheckResult:
        if article.published_at is not None:
            return CheckResult(self.name, self.dimension, Status.PASS, "Date is present")
        return CheckResult(self.name, self.dimension, Status.FAIL, "Publication date is missing")
