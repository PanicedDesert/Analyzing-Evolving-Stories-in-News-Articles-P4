from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Sequence, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from avis.nlp.preprocess import clean_documents


@dataclass
class TfidfConfig:
    max_features: int = 100_000
    max_df: float = 0.8
    min_df: int = 5
    ngram_range: Tuple[int, int] = (1, 3)


def fit_tfidf(
    docs: Iterable[str],
    stopwords: Sequence[str],
    config: Optional[TfidfConfig] = None,
) -> tuple[TfidfVectorizer, np.ndarray]:
    """Clean docs and fit a TF-IDF vectorizer.

    Returns
    -------
    vectorizer, X
        `X` is a dense numpy array (for simplicity). For large corpora you
        should keep the sparse matrix instead.
    """
    cfg = config or TfidfConfig()
    cleaned = clean_documents(docs, stopwords)

    vectorizer = TfidfVectorizer(
        lowercase=True,
        max_features=cfg.max_features,
        max_df=cfg.max_df,
        min_df=cfg.min_df,
        ngram_range=cfg.ngram_range,
        stop_words=None,
    )

    X_sparse = vectorizer.fit_transform(cleaned)
    X = X_sparse.toarray()
    return vectorizer, X
