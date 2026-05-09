from __future__ import annotations

from fastapi import APIRouter

from dashboard.backend.database import get_cursor

router = APIRouter(tags=["stats"])


@router.get("/stats")
def get_stats():
    """Global KPIs: total articles, sources, languages, latest scrape."""
    with get_cursor() as cur:
        cur.execute("""
            SELECT
                COUNT(*)                                              AS total_articles,
                COUNT(DISTINCT source)                                AS total_sources,
                COUNT(DISTINCT language) FILTER (WHERE language IS NOT NULL) AS total_languages,
                MAX(scraped_at)                                       AS latest_scrape,
                MIN(published_at)                                     AS earliest_article,
                MAX(published_at)                                     AS latest_article
            FROM articles
        """)
        row = cur.fetchone()

    return {
        "total_articles": row["total_articles"],
        "total_sources": row["total_sources"],
        "total_languages": row["total_languages"],
        "latest_scrape": row["latest_scrape"].isoformat() if row["latest_scrape"] else None,
        "earliest_article": row["earliest_article"].isoformat() if row["earliest_article"] else None,
        "latest_article": row["latest_article"].isoformat() if row["latest_article"] else None,
    }
