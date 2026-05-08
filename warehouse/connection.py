from __future__ import annotations

import psycopg2

from shared.config import config
from shared.exceptions import WarehouseError
from shared.logging import get_logger

_log = get_logger(__name__)


def get_connection():
    """Return a new database connection. Caller is responsible for closing it."""
    try:
        conn = psycopg2.connect(
            host=config.postgres.host,
            port=config.postgres.port,
            dbname=config.postgres.database,
            user=config.postgres.user,
            password=config.postgres.password,
        )
        conn.autocommit = False
        return conn
    except psycopg2.Error as exc:
        raise WarehouseError(f"Failed to connect to database: {exc}") from exc
