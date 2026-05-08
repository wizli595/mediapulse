from __future__ import annotations

from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException


def detect_language(text: str) -> str | None:
    """Detect the language of a text. Returns ISO 639-1 code or None."""
    if not text or len(text) < 20:
        return None
    try:
        return detect(text)
    except LangDetectException:
        return None
