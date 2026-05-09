from __future__ import annotations

from fastapi import APIRouter

from dashboard.backend.database import get_cursor

router = APIRouter(tags=["sources"])


@router.get("/sources")
def get_sources():
    """Article count and latest article per source. For bar chart."""
    with get_cursor() as cur:
        cur.execute("""
            SELECT source, COUNT(*) AS count, MAX(published_at) AS latest
            FROM articles
            GROUP BY source
            ORDER BY count DESC
        """)
        rows = cur.fetchall()

    return [
        {
            "source": r["source"],
            "count": r["count"],
            "latest": r["latest"].isoformat() if r["latest"] else None,
        }
        for r in rows
    ]


@router.get("/sources/{source}/languages")
def get_source_languages(source: str):
    """Language breakdown for a specific source."""
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT language, COUNT(*) AS count
            FROM articles
            WHERE source = %s AND language IS NOT NULL
            GROUP BY language
            ORDER BY count DESC
            """,
            (source,),
        )
        rows = cur.fetchall()

    return [{"language": r["language"], "count": r["count"]} for r in rows]
