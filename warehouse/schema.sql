-- MediaPulse Data Warehouse Schema

CREATE TABLE IF NOT EXISTS articles (
    article_id    VARCHAR(16) PRIMARY KEY,
    title         TEXT NOT NULL,
    author        TEXT,
    published_at  TIMESTAMP NOT NULL,
    category      TEXT,
    content       TEXT NOT NULL,
    source        VARCHAR(50) NOT NULL,
    url           TEXT NOT NULL UNIQUE,
    language      VARCHAR(10),
    scraped_at    TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS trends (
    id             SERIAL PRIMARY KEY,
    date           DATE NOT NULL,
    source         VARCHAR(50) NOT NULL,
    category       TEXT,
    article_count  INTEGER NOT NULL,
    UNIQUE (date, source, category)
);

CREATE TABLE IF NOT EXISTS topics (
    id         SERIAL PRIMARY KEY,
    keyword    TEXT NOT NULL,
    frequency  INTEGER NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS source_counts (
    source         VARCHAR(50) PRIMARY KEY,
    article_count  INTEGER NOT NULL,
    updated_at     TIMESTAMP DEFAULT NOW()
);

-- Indexes for dashboard queries
CREATE INDEX IF NOT EXISTS idx_articles_source ON articles (source);
CREATE INDEX IF NOT EXISTS idx_articles_published ON articles (published_at);
CREATE INDEX IF NOT EXISTS idx_articles_category ON articles (category);
CREATE INDEX IF NOT EXISTS idx_trends_date ON trends (date);
