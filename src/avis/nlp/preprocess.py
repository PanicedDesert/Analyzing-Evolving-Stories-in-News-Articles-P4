from __future__ import annotations

import string
from typing import Iterable, List, Sequence


def normalize_token(token: str) -> str:
    """Lowercase a token and strip punctuation/digits."""
    token = str(token).lower()
    token = token.translate(str.maketrans("", "", string.punctuation))
    token = token.translate(str.maketrans("", "", "0123456789"))
    return token.strip()


def remove_stopwords(text: str, stopwords: Sequence[str]) -> str:
    """Remove stopwords after simple normalization.

    This mirrors the original logic used in `Model code/k_means_model.py`.
    """
    words = str(text).split()
    kept: List[str] = []
    stop = set(stopwords)
    for w in words:
        w2 = normalize_token(w)
        if not w2:
            continue
        if w2 not in stop:
            kept.append(w2)
    out = " ".join(kept)
    while "  " in out:
        out = out.replace("  ", " ")
    return out


def clean_documents(docs: Iterable[str], stopwords: Sequence[str]) -> List[str]:
    """Clean a sequence of documents."""
    return [remove_stopwords(doc, stopwords) for doc in docs]
