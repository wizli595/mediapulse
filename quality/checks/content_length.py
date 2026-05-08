from __future__ import annotations

from quality.checks.base import AbstractCheck, CheckResult, Dimension, Status
from shared.models import Article

MIN_CONTENT_LENGTH = 50


class ContentLengthCheck(AbstractCheck):

    @property
    def name(self) -> str:
        return "content_length"

    @property
    def dimension(self) -> Dimension:
        return Dimension.VALIDITY

    def run(self, article: Article) -> CheckResult:
        length = len(article.content.strip()) if article.content else 0
        if length >= MIN_CONTENT_LENGTH:
            return CheckResult(self.name, self.dimension, Status.PASS, f"Content length OK ({length} chars)")
        return CheckResult(self.name, self.dimension, Status.FAIL, f"Content too short ({length} chars, min {MIN_CONTENT_LENGTH})")
