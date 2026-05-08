from __future__ import annotations

from io import BytesIO

from minio import Minio
from minio.error import S3Error

from shared.config import config
from shared.exceptions import StorageError
from shared.logging import get_logger
from storage.base import AbstractStorage

_log = get_logger(__name__)

_LAYER_BUCKETS = {
    "bronze": config.minio.bucket_bronze,
    "silver": config.minio.bucket_silver,
    "gold": config.minio.bucket_gold,
}


class MinIOStorage(AbstractStorage):

    def __init__(self) -> None:
        self._client = Minio(
            endpoint=config.minio.endpoint,
            access_key=config.minio.access_key,
            secret_key=config.minio.secret_key,
            secure=config.minio.secure,
        )

    def _bucket(self, layer: str) -> str:
        bucket = _LAYER_BUCKETS.get(layer)
        if not bucket:
            raise StorageError(f"Unknown layer: {layer}. Must be one of {list(_LAYER_BUCKETS)}")
        return bucket

    def write(self, layer: str, key: str, data: bytes) -> None:
        bucket = self._bucket(layer)
        try:
            self._client.put_object(bucket, key, BytesIO(data), length=len(data))
            _log.info("Wrote %s/%s (%d bytes)", bucket, key, len(data))
        except S3Error as exc:
            raise StorageError(f"Failed to write {bucket}/{key}: {exc}") from exc

    def read(self, layer: str, key: str) -> bytes:
        bucket = self._bucket(layer)
        try:
            response = self._client.get_object(bucket, key)
            data = response.read()
            response.close()
            response.release_conn()
            return data
        except S3Error as exc:
            raise StorageError(f"Failed to read {bucket}/{key}: {exc}") from exc

    def list_keys(self, layer: str, prefix: str = "") -> list[str]:
        bucket = self._bucket(layer)
        try:
            objects = self._client.list_objects(bucket, prefix=prefix, recursive=True)
            return [obj.object_name for obj in objects]
        except S3Error as exc:
            raise StorageError(f"Failed to list {bucket}/{prefix}: {exc}") from exc

    def exists(self, layer: str, key: str) -> bool:
        bucket = self._bucket(layer)
        try:
            self._client.stat_object(bucket, key)
            return True
        except S3Error:
            return False

    def delete(self, layer: str, key: str) -> None:
        bucket = self._bucket(layer)
        try:
            self._client.remove_object(bucket, key)
            _log.info("Deleted %s/%s", bucket, key)
        except S3Error as exc:
            raise StorageError(f"Failed to delete {bucket}/{key}: {exc}") from exc
