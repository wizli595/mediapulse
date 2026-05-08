from __future__ import annotations

from minio import Minio

from shared.config import config
from shared.logging import get_logger

_log = get_logger(__name__)

BUCKETS = [
    config.minio.bucket_bronze,
    config.minio.bucket_silver,
    config.minio.bucket_gold,
]


def setup_buckets() -> None:
    """Create bronze/silver/gold buckets in MinIO if they don't exist."""
    client = Minio(
        endpoint=config.minio.endpoint,
        access_key=config.minio.access_key,
        secret_key=config.minio.secret_key,
        secure=config.minio.secure,
    )

    for bucket in BUCKETS:
        if not client.bucket_exists(bucket):
            client.make_bucket(bucket)
            _log.info("Created bucket: %s", bucket)
        else:
            _log.info("Bucket already exists: %s", bucket)


if __name__ == "__main__":
    setup_buckets()
