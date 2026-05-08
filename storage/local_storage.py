from __future__ import annotations

from pathlib import Path

from shared.exceptions import StorageError
from shared.logging import get_logger
from storage.base import AbstractStorage

_log = get_logger(__name__)


class LocalStorage(AbstractStorage):
    """File-system backed storage. Used for dev/testing without MinIO."""

    def __init__(self, root: Path) -> None:
        self._root = root

    def _path(self, layer: str, key: str) -> Path:
        return self._root / layer / key

    def write(self, layer: str, key: str, data: bytes) -> None:
        path = self._path(layer, key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        _log.info("Wrote %s/%s (%d bytes)", layer, key, len(data))

    def read(self, layer: str, key: str) -> bytes:
        path = self._path(layer, key)
        if not path.exists():
            raise StorageError(f"Object not found: {layer}/{key}")
        return path.read_bytes()

    def list_keys(self, layer: str, prefix: str = "") -> list[str]:
        layer_dir = self._root / layer
        if not layer_dir.exists():
            return []
        return [
            key
            for p in layer_dir.rglob("*")
            if p.is_file()
            for key in [str(p.relative_to(layer_dir)).replace("\\", "/")]
            if key.startswith(prefix)
        ]

    def exists(self, layer: str, key: str) -> bool:
        return self._path(layer, key).exists()

    def delete(self, layer: str, key: str) -> None:
        path = self._path(layer, key)
        if path.exists():
            path.unlink()
            _log.info("Deleted %s/%s", layer, key)
