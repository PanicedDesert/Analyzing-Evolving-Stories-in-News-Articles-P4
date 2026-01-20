# avis (refactored)

This repository is a refactor of the original `avis-main` project into a
maintainable Python package (no notebooks required to run core code).

The original repository mixed:
- notebooks (analysis + experiments)
- scripts with hard-coded relative paths
- model logic without a clear module structure

This refactor keeps **all original work** under `original/` and introduces a
clean `src/` layout for reusable code.

## Methodology (what the code is doing)

At a high level, this project is about representing Danish news/article text as
features, and then:
1) clustering documents into themes/topics (KMeans over TF-IDF), and/or
2) running supervised models (in the original scripts), and
3) experimenting with search/sweep methods (beam search, parameter sweep) as
notebook workflows.

### Text processing
- normalize tokens (lowercase, strip punctuation/digits)
- remove Danish stopwords (bundled as `avis/data/stopwords_da.txt`)
- output cleaned documents as strings

### Vectorization (TF-IDF)
- fit a `TfidfVectorizer` with configurable `max_df`, `min_df`, `ngram_range`, etc.
- produce a document-term feature matrix

### Clustering (KMeans)
- fit KMeans on TF-IDF features
- extract top terms per cluster to interpret learned topics

## Repository structure

```
avis-refactored-v2/
├── src/
│   └── avis/
│       ├── nlp/
│       │   ├── preprocess.py
│       │   └── stopwords.py
│       ├── models/
│       │   ├── vectorize_tfidf.py
│       │   └── kmeans_topics.py
│       ├── experiments/
│       │   ├── beamsearch.py
│       │   └── parameter_search.py
│       └── data/
│           └── stopwords_da.txt
├── original/
│   └── (your original notebooks + scripts, unmodified)
├── pyproject.toml
└── README.md
```

## Install

From the repo root:

```bash
pip install -e .
```

## Example usage

### TF-IDF + KMeans topics

```python
from avis.nlp.stopwords import load_danish_stopwords
from avis.models.vectorize_tfidf import fit_tfidf, TfidfConfig
from avis.models.kmeans_topics import fit_kmeans_topics, top_terms_per_cluster, KMeansTopicConfig

stop = load_danish_stopwords()

docs = [
    "Dette er en artikel om politik og økonomi...",
    "Sport og fodbold nyheder...",
]

vectorizer, X = fit_tfidf(docs, stop, TfidfConfig(max_features=5000))
model = fit_kmeans_topics(X, KMeansTopicConfig(n_clusters=2))
print(top_terms_per_cluster(model, vectorizer, top_n=8))
```

## About the experiments folder

The two experiment modules are currently **scaffolding only**:
- `avis.experiments.beamsearch` corresponds to the notebook
  `BEAMSEARCH_WITH_LOOKAHEAD_sigmoid.ipynb`
- `avis.experiments.parameter_search` corresponds to
  `Parameter_search_til_rapport.ipynb`

Porting the notebooks into these modules is the next step if you want a fully
reproducible, CLI-driven pipeline.
