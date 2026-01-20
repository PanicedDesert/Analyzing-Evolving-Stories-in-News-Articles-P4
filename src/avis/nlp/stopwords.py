from __future__ import annotations

from importlib import resources
from typing import List


def load_danish_stopwords() -> List[str]:
    """Load Danish stopwords bundled with the package."""
    path = resources.files("avis").joinpath("data/stopwords_da.txt")
    text = path.read_text(encoding="utf-8")
    return [line.strip() for line in text.splitlines() if line.strip()]
