from processing.silver.html_cleaner import strip_html
from processing.silver.text_normalizer import normalize_text
from processing.silver.language_detector import detect_language
from processing.silver.deduplicator import is_duplicate
from processing.silver.pipeline import process_to_silver


def test_strip_html_removes_tags():
    assert strip_html("<p>Hello <b>world</b></p>") == "Hello world"


def test_strip_html_decodes_entities():
    assert strip_html("A &amp; B &lt; C") == "A & B < C"


def test_strip_html_empty():
    assert strip_html("") == ""


def test_strip_html_plain_text():
    assert strip_html("No HTML here") == "No HTML here"


def test_normalize_collapses_whitespace():
    assert normalize_text("hello    world") == "hello world"


def test_normalize_strips_control_chars():
    result = normalize_text("hello\x00world\x07test")
    assert "\x00" not in result
    assert "\x07" not in result


def test_normalize_collapses_newlines():
    result = normalize_text("a\n\n\n\n\nb")
    assert result == "a\n\nb"


def test_detect_language_english():
    text = "The president announced new economic policies for the country today."
    assert detect_language(text) == "en"


def test_detect_language_arabic():
    text = "أعلن الرئيس عن سياسات اقتصادية جديدة للبلاد اليوم في مؤتمر صحفي كبير"
    assert detect_language(text) == "ar"


def test_detect_language_short_text():
    assert detect_language("hi") is None


def test_detect_language_empty():
    assert detect_language("") is None


def test_is_duplicate_false(sample_article, tmp_storage):
    assert not is_duplicate(sample_article, tmp_storage)


def test_is_duplicate_true(sample_article, tmp_storage):
    # Write it to silver first
    date_prefix = sample_article.published_at.strftime("%Y/%m/%d")
    key = f"{sample_article.source}/{date_prefix}/{sample_article.article_id}.json"
    tmp_storage.write("silver", key, b"exists")

    assert is_duplicate(sample_article, tmp_storage)


def test_pipeline_writes_to_silver(sample_article, tmp_storage):
    result = process_to_silver(sample_article, tmp_storage)
    assert result is not None
    assert result.language is not None
    assert len(tmp_storage.list_keys("silver")) == 1


def test_pipeline_skips_duplicate(sample_article, tmp_storage):
    process_to_silver(sample_article, tmp_storage)
    result = process_to_silver(sample_article, tmp_storage)
    assert result is None
