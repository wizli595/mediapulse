from processing.gold.trend_aggregator import compute_trends
from processing.gold.topic_extractor import extract_topics
from processing.gold.source_counter import count_by_source
from processing.gold.pipeline import process_to_gold


def test_compute_trends(article_list):
    trends = compute_trends(article_list)
    assert len(trends) > 0

    total = sum(t.article_count for t in trends)
    assert total == len(article_list)


def test_compute_trends_groups_by_source(article_list):
    trends = compute_trends(article_list)
    sources = {t.source for t in trends}
    assert "hespress" in sources
    assert "bbc" in sources


def test_extract_topics(article_list):
    topics = extract_topics(article_list, top_n=10)
    assert len(topics) > 0
    assert topics[0].frequency >= topics[-1].frequency


def test_extract_topics_filters_stopwords(article_list):
    topics = extract_topics(article_list)
    keywords = {t.keyword for t in topics}
    assert "the" not in keywords
    assert "and" not in keywords


def test_count_by_source(article_list):
    counts = count_by_source(article_list)
    assert len(counts) == 3  # hespress, bbc, cnn

    hespress = next(c for c in counts if c.source == "hespress")
    assert hespress.article_count == 2


def test_process_to_gold(article_list, tmp_storage):
    process_to_gold(article_list, tmp_storage)

    assert tmp_storage.exists("gold", "trends.json")
    assert tmp_storage.exists("gold", "topics.json")
    assert tmp_storage.exists("gold", "sources.json")


def test_process_to_gold_empty(tmp_storage):
    process_to_gold([], tmp_storage)
    assert tmp_storage.list_keys("gold") == []
