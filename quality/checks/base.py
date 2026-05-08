from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from shared.models import Article


class Dimension(Enum):
    COMPLETENESS = "completeness"
    CONSISTENCY = "consistency"
    VALIDITY = "validity"


class Status(Enum):
    PASS = "pass"
    FAIL = "fail"


@dataclass(frozen=True)
class CheckResult:
    check_name: str
    dimension: Dimension
    status: Status
    message: str


class AbstractCheck(ABC):
    """Contract for a single data quality check.

    Each check validates ONE rule against ONE article.
    It does not fix, transform, or skip — only report.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of this check."""

    @property
    @abstractmethod
    def dimension(self) -> Dimension:
        """Quality dimension this check belongs to."""

    @abstractmethod
    def run(self, article: Article) -> CheckResult:
        """Run this check against one article."""
