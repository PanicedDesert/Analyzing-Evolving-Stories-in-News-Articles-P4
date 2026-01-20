# **avis — Analyzing Evolving Stories in News Articles (Refactored)**

> **Research-driven NLP + Optimization for Story Evolution**

---
## 🔹 Abstract (from the paper)
> There is an overwhelming number of news articles published every day. Tracking how a news story *evolves over time* is difficult because similarity-based methods tend to circle around the same event instead of revealing its historical origins. This project implements and extends a framework that **mines historical news to detect the origin of events, segments timelines into coherent phases, and identifies the most relevant documents at each turning point**. The approach combines NLP preprocessing, topic modeling, and a continuous optimization formulation that balances **coherence, diffusion, temporal structure, and document relevance**. Quantitative metrics and human evaluations show that the method discovers statistically significant and meaningful storylines in reasonable time, with potential for predicting future entities in evolving stories.

*(Summarized from Barranco et al., 2017) — see Fig. 1 in the paper for diffusion vs similarity-based storytelling.*

---
## 🎯 What this project is about (for recruiters)

This repository is a **clean, production-style refactor** of a research prototype for:

- **News story evolution analysis**
- **Entity-centric NLP and topic modeling (LDA, TF–IDF)**
- **Graph/optimization-based storytelling (“connecting the dots”)**
- **Continuous-time segmentation of document streams**
- **Relevance-weighted document selection**
- **Statistical validation and human-in-the-loop evaluation**
- **Downstream prediction of future entities from past story evolution**

If you care about keywords: **NLP, text mining, topic modeling, optimization, temporal modeling, document networks, L-BFGS-B, causal diffusion, information retrieval, explainable AI, data science.**

---
## 🧠 Conceptual Methodology (high-level, non-technical)

### 1️⃣ Preprocessing (Fig. 2 — Framework Diagram)
*(See the pipeline on page 3 of the paper)*
- Extract named entities (persons, organizations, locations)
- Represent documents with **TF–IDF over entities**
- Fit **LDA topic models** to obtain document topic distributions
- Filter candidate documents using **temporal + topical constraints** (KL-divergence threshold)

### 2️⃣ Story Generation (Core Contribution)
The system finds a sequence of **turning points in time** and assigns documents to time segments using a **smooth membership function** (Fig. 3 in the paper). It jointly optimizes:

- **Incoherence (within segments)** — documents in the same phase should be similar
- **Unconnectedness / Similarity penalty (across segments)** — different phases should represent different events
- **Temporal penalty** — discourages grouping far-apart documents
- **Overlap penalty** — prevents turning points from collapsing together (Fig. 4)
- **Relevance weights** — highlights the most important documents per segment
- **Uniformity penalty** — avoids trivial solutions (all documents selected or none)

The final objective (Eq. 21) is optimized using **L-BFGS-B (bounded quasi-Newton)**.

---
## 📊 Key Results (visuals from the paper)

### 🔹 Diffusion vs Similarity (Fig. 1, p.1)
- **Diffusion-based approach** captures *smooth historical evolution* across different but related events.
- **Similarity-based approach** tends to stay within a narrow topic window.

### 🔹 Human Evaluation (Fig. 5, p.6)
Users rated generated chains on:
- Familiarity
- Coherence
- Relevance
- Broadness

Average scores were consistently **above 3/5**, indicating meaningful and interpretable storylines.

### 🔹 Dispersion Comparison (Fig. 6, p.6)
The proposed method achieves **higher dispersion coefficients** than:
- K-means clustering
- Pure similarity chaining

This suggests better coverage of evolving events rather than repetition of similar articles.

### 🔹 Case Study: Brexit Timeline (Fig. 7, p.7)
Compared multiple objective formulations. The final diffusion-based method produced the **most coherent multi-event narrative**, linking:
- Eurozone crisis → German austerity → EU tensions → Immigration → Brexit.

### 🔹 Statistical Significance (Fig. 8, p.8)
Turning points remained statistically significant across changes in:
- Gamma variance (membership smoothness)
- Topical divergence threshold
- Overlap penalty

### 🔹 Repeatability (Fig. 9, p.8)
Multiple optimization runs yield **stable turning points**, especially with reasonable distance thresholds.

### 🔹 Prediction Experiment (Fig. 10, p.9)
Relevant past documents were used to **predict future entity weights** via linear regression. Even a simple model recovered key entities (e.g., *Paris, Belgium*) 4–10 days ahead.

---
## 🏗 Repository structure (clean, maintainable)
```
avis-refactored/
├── src/avis/
│   ├── nlp/           # tokenization, stopwords, preprocessing
│   ├── models/        # TF–IDF, KMeans topic tools
│   ├── experiments/   # beam search & parameter sweep scaffolding
│   └── data/          # Danish stopwords
├── original/          # your original notebooks (untouched)
├── pyproject.toml
└── README.md
```

---
## 🚀 Installation
```bash
pip install -e .
```

## 🧪 Minimal example (TF–IDF + KMeans topics)
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

---
## 🏁 Conclusion (from the paper)
> The framework successfully uncovers the historical evolution of news stories from large archives. It not only reconstructs meaningful timelines but also enables **future entity prediction** from past diffusion patterns. The authors propose extending the work toward early-warning systems for emerging events and incorporating **interactive user feedback** to adapt the optimization to human expectations.

---
## 📚 Reference
Barranco, R. C., Boedihardjo, A. P., & Hossain, M. S. (2017). *Analyzing Evolving Stories in News Articles*. ACM Conference.

