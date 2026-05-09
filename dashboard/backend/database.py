from __future__ import annotations

from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool

from shared.config import config

_pool: ThreadedConnectionPool | None = None


def _get_pool() -> ThreadedConnectionPool:
    """Lazy-init a thread-safe connection pool. Reuses connections across requests."""
    global _pool
    if _pool is None:
        _pool = ThreadedConnectionPool(
            minconn=2,
            maxconn=10,
            host=config.postgres.host,
            port=config.postgres.port,
            dbname=config.postgres.database,
            user=config.postgres.user,
            password=config.postgres.password,
        )
    return _pool


@contextmanager
def get_cursor():
    """Yield a dict cursor from the pool. Connection is returned automatically."""
    pool = _get_pool()
    conn = pool.getconn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        pool.putconn(conn)
