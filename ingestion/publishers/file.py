from __future__ import annotations

from pathlib import Path

from ingestion.publishers.base import AbstractPublisher
from ingestion.serializers.article import article_to_json
from shared.logging import get_logger
from shared.models import Article

_log = get_logger(__name__)


class FilePublisher(AbstractPublisher):
    """Writes articles as JSON lines to a file. Used for dev/testing without Kafka."""

    def __init__(self, output_path: Path) -> None:
        self._path = output_path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._file = open(self._path, "a", encoding="utf-8")

    def publish(self, article: Article) -> None:
        self._file.write(article_to_json(article) + "\n")
        self._file.flush()
        _log.info("Wrote article %s to %s", article.article_id, self._path)

    def close(self) -> None:
        self._file.close()
        _log.info("File publisher closed: %s", self._path)
