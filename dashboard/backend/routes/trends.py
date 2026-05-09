from __future__ import annotations

from fastapi import APIRouter, Query

from dashboard.backend.database import get_cursor

router = APIRouter(tags=["trends"])


@router.get("/trends")
def get_trends(days: int = Query(default=30, le=365)):
    """Articles per day, grouped by source. For line/area charts."""
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT DATE(published_at) AS day, source, COUNT(*) AS count
            FROM articles
            WHERE published_at >= CURRENT_DATE - make_interval(days => %s)
            GROUP BY day, source
            ORDER BY day
            """,
            (days,),
        )
        rows = cur.fetchall()

    return [
        {"date": str(r["day"]), "source": r["source"], "count": r["count"]}
        for r in rows
    ]


@router.get("/trends/categories")
def get_category_trends(days: int = Query(default=30, le=365)):
    """Articles per category over time."""
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT category, COUNT(*) AS count
            FROM articles
            WHERE published_at >= CURRENT_DATE - make_interval(days => %s)
              AND category IS NOT NULL
            GROUP BY category
            ORDER BY count DESC
            LIMIT 15
            """,
            (days,),
        )
        rows = cur.fetchall()

    return [{"category": r["category"], "count": r["count"]} for r in rows]
