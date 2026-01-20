#  TOPIC MODELING/TEXT CLASS. SERIES  #
#             Lesson 02.03            #
# TF-IDF in Python with Scikit Learn  #
#               with                  #
#        Dr. W.J.B. Mattingly         #
import test
import pandas as pd
import ownfunc
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import string
import json
import glob
import joblib
import pickle
from joblib import dump, load


stopwords_danish = ownfunc.stopword_reader()


def remove_stops(text, stops):
    words = text.split()
    final = []
    for word in words:
        word =str(word)
        #print("foer", word, " ", end="")
        word = word.lower()
        word = word.translate(str.maketrans("", "", string.punctuation))
        word = word.translate(str.maketrans("", "", "01234566789"))
        #print("- ", word)
        if word not in stops:
            final.append(word)
    final = " ".join(final)  # joins all the words again
    while "  " in final:
        # removes double spacings until no double spacing are present
        final = final.replace("  ", " ")
    return (final)


def clean_docs(docs):
    stops = stopwords_danish
    final = []
    for doc in docs:
        clean_doc = remove_stops(doc, stops)
        final.append(clean_doc)
    return (final)


list_docs = test.get_text_doc(test.json_dataset,
             test.popular_categories, find_categories=False)

print("listdoc:",list_docs[:2])

cleaned_docs = clean_docs(list_docs)

vectorizer = TfidfVectorizer(
    lowercase=True,
    max_features=100,
    max_df=0.8,
    min_df=5,
    ngram_range=(1, 3),
    stop_words=None

)

vectors = vectorizer.fit_transform(cleaned_docs)

feature_names = vectorizer.get_feature_names_out()

dense = vectors.todense()
denselist = dense.tolist()
print("did vectorise")
all_keywords = []

for description in denselist:
    x = 0
    keywords = []
    for word in description:
        if word > 0:
            keywords.append(feature_names[x])
        x = x+1
    all_keywords.append(keywords)

print(test.popular_categorie_count)
true_k = test.popular_categorie_count
print("true k:", true_k )

model = KMeans(n_clusters=true_k, init="k-means++", max_iter=1000, n_init=1)

model.fit(vectors)

order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names_out()

with open("results.txt", "w", encoding="utf-8") as f:
    for i in range(true_k):
        print("printing")
        f.write(f"Cluster {i}")
        f.write("\n")
        for ind in order_centroids[i, :10]:
            print("ind:",terms[ind])
            f.write(' %s' % terms[ind],)
            f.write("\n")
        f.write("\n")
        f.write("\n")

dump(model, 'filename.joblib') 
#https://scikit-learn.org/stable/model_persistence.html
