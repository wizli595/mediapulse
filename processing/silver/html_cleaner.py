from __future__ import annotations

import re


def strip_html(text: str) -> str:
    """Remove HTML tags and decode entities from raw text."""
    cleaned = re.sub(r"<[^>]+>", "", text)
    cleaned = re.sub(r"&nbsp;", " ", cleaned)
    cleaned = re.sub(r"&amp;", "&", cleaned)
    cleaned = re.sub(r"&lt;", "<", cleaned)
    cleaned = re.sub(r"&gt;", ">", cleaned)
    cleaned = re.sub(r"&quot;", '"', cleaned)
    cleaned = re.sub(r"&#\d+;", "", cleaned)
    return cleaned.strip()
