from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence, Tuple

import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer


@dataclass
class KMeansTopicConfig:
    n_clusters: int
    max_iter: int = 1000
    n_init: int = 10
    random_state: int = 0


def top_terms_per_cluster(
    model: KMeans,
    vectorizer: TfidfVectorizer,
    top_n: int = 10,
) -> List[List[str]]:
    terms = vectorizer.get_feature_names_out()
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    out: List[List[str]] = []
    for i in range(order_centroids.shape[0]):
        out.append([terms[ind] for ind in order_centroids[i, :top_n]])
    return out


def fit_kmeans_topics(
    X: np.ndarray,
    config: KMeansTopicConfig,
) -> KMeans:
    """Fit a KMeans topic model on TF-IDF features."""
    model = KMeans(
        n_clusters=config.n_clusters,
        init="k-means++",
        max_iter=config.max_iter,
        n_init=config.n_init,
        random_state=config.random_state,
    )
    model.fit(X)
    return model
