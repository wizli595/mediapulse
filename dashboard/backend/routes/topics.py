from __future__ import annotations

from fastapi import APIRouter, Query

from dashboard.backend.database import get_cursor

router = APIRouter(tags=["topics"])


@router.get("/topics")
def get_topics(limit: int = Query(default=30, le=100)):
    """Top keywords by frequency. For bar chart / word cloud."""
    with get_cursor() as cur:
        cur.execute(
            "SELECT keyword, frequency FROM topics ORDER BY frequency DESC LIMIT %s",
            (limit,),
        )
        rows = cur.fetchall()

    return [{"keyword": r["keyword"], "frequency": r["frequency"]} for r in rows]
