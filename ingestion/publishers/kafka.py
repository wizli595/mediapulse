from __future__ import annotations

from kafka import KafkaProducer

from ingestion.publishers.base import AbstractPublisher
from ingestion.serializers.article import article_to_bytes
from shared.config import config
from shared.exceptions import IngestionError
from shared.logging import get_logger
from shared.models import Article

_log = get_logger(__name__)


class KafkaPublisher(AbstractPublisher):

    def __init__(self) -> None:
        try:
            self._producer = KafkaProducer(
                bootstrap_servers=config.kafka.bootstrap_servers,
                value_serializer=lambda v: v,
            )
            self._topic = config.kafka.topic_raw_articles
        except Exception as exc:
            raise IngestionError(f"Failed to connect to Kafka: {exc}") from exc

    def publish(self, article: Article) -> None:
        try:
            self._producer.send(
                self._topic,
                value=article_to_bytes(article),
                key=article.article_id.encode("utf-8"),
            )
            self._producer.flush()
            _log.info("Published article %s to topic %s", article.article_id, self._topic)
        except Exception as exc:
            raise IngestionError(f"Failed to publish article {article.article_id}: {exc}") from exc

    def close(self) -> None:
        self._producer.close()
        _log.info("Kafka producer closed")
