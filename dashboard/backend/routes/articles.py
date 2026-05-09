from __future__ import annotations

from fastapi import APIRouter, Query

from dashboard.backend.database import get_cursor

router = APIRouter(tags=["articles"])


@router.get("/articles")
def get_articles(
    source: str | None = None,
    category: str | None = None,
    language: str | None = None,
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0),
):
    """Paginated article list with optional filters."""
    conditions = []
    params: list = []

    if source:
        conditions.append("source = %s")
        params.append(source)
    if category:
        conditions.append("category = %s")
        params.append(category)
    if language:
        conditions.append("language = %s")
        params.append(language)

    where = "WHERE " + " AND ".join(conditions) if conditions else ""

    with get_cursor() as cur:
        cur.execute(
            f"SELECT COUNT(*) AS total FROM articles {where}",
            params,
        )
        total = cur.fetchone()["total"]

        cur.execute(
            f"""
            SELECT article_id, title, source, category, language, author, published_at, url
            FROM articles {where}
            ORDER BY published_at DESC
            LIMIT %s OFFSET %s
            """,
            params + [limit, offset],
        )
        rows = cur.fetchall()

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "articles": [
            {
                "article_id": r["article_id"],
                "title": r["title"],
                "source": r["source"],
                "category": r["category"],
                "language": r["language"],
                "author": r["author"],
                "published_at": r["published_at"].isoformat() if r["published_at"] else None,
                "url": r["url"],
            }
            for r in rows
        ],
    }
