-- ================================================
-- MediaPulse — Metabase Dashboard Queries
-- Import these as "Native queries" in Metabase.
-- ================================================

-- ============================================
-- DASHBOARD 1: News Trends
-- ============================================

-- 1.1 Articles per day (line chart)
SELECT DATE(published_at) AS day, COUNT(*) AS articles
FROM articles
GROUP BY day
ORDER BY day DESC
LIMIT 30;

-- 1.2 Articles per day per source (stacked area)
SELECT DATE(published_at) AS day, source, COUNT(*) AS articles
FROM articles
GROUP BY day, source
ORDER BY day DESC;

-- 1.3 Trending categories today
SELECT category, COUNT(*) AS articles
FROM articles
WHERE DATE(published_at) = CURRENT_DATE AND category IS NOT NULL
GROUP BY category
ORDER BY articles DESC
LIMIT 10;

-- ============================================
-- DASHBOARD 2: Articles per Source
-- ============================================

-- 2.1 Total articles per source (bar chart)
SELECT source, COUNT(*) AS total_articles
FROM articles
GROUP BY source
ORDER BY total_articles DESC;

-- 2.2 Source breakdown by language (stacked bar)
SELECT source, language, COUNT(*) AS articles
FROM articles
WHERE language IS NOT NULL
GROUP BY source, language
ORDER BY source, articles DESC;

-- 2.3 Source freshness (latest article per source)
SELECT source, MAX(published_at) AS latest_article, COUNT(*) AS total
FROM articles
GROUP BY source
ORDER BY latest_article DESC;

-- ============================================
-- DASHBOARD 3: Top Keywords
-- ============================================

-- 3.1 Most frequent keywords (word cloud / bar chart)
SELECT keyword, frequency
FROM topics
ORDER BY frequency DESC
LIMIT 30;

-- 3.2 Trend evolution by date and source
SELECT date, source, category, article_count
FROM trends
ORDER BY date DESC, article_count DESC;

-- ============================================
-- DASHBOARD 4: Data Quality
-- ============================================

-- 4.1 Articles missing category
SELECT source, COUNT(*) AS missing_category
FROM articles
WHERE category IS NULL
GROUP BY source
ORDER BY missing_category DESC;

-- 4.2 Articles with short content
SELECT source, COUNT(*) AS short_articles
FROM articles
WHERE LENGTH(content) < 100
GROUP BY source
ORDER BY short_articles DESC;

-- 4.3 Language distribution
SELECT language, COUNT(*) AS articles
FROM articles
WHERE language IS NOT NULL
GROUP BY language
ORDER BY articles DESC;
