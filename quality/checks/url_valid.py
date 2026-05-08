from __future__ import annotations

from urllib.parse import urlparse

from quality.checks.base import AbstractCheck, CheckResult, Dimension, Status
from shared.models import Article


class UrlValidCheck(AbstractCheck):

    @property
    def name(self) -> str:
        return "url_valid"

    @property
    def dimension(self) -> Dimension:
        return Dimension.CONSISTENCY

    def run(self, article: Article) -> CheckResult:
        parsed = urlparse(article.url)
        if parsed.scheme in ("http", "https") and parsed.netloc:
            return CheckResult(self.name, self.dimension, Status.PASS, "URL is valid")
        return CheckResult(self.name, self.dimension, Status.FAIL, f"Invalid URL: {article.url}")
