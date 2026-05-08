from __future__ import annotations

from quality.checks.base import AbstractCheck, CheckResult, Dimension, Status
from shared.models import Article


class TitlePresentCheck(AbstractCheck):

    @property
    def name(self) -> str:
        return "title_present"

    @property
    def dimension(self) -> Dimension:
        return Dimension.COMPLETENESS

    def run(self, article: Article) -> CheckResult:
        if article.title and article.title.strip():
            return CheckResult(self.name, self.dimension, Status.PASS, "Title is present")
        return CheckResult(self.name, self.dimension, Status.FAIL, "Title is missing or empty")
