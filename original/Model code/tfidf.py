import pandas as pd
import ownfunc
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import string
import json
import glob
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from Bowmodel.bow import Vectorize_Own_Script
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC, LinearSVC
import numpy as np
import pickle



stopwords_danish = ownfunc.stopword_reader()



# Replace 'your_file.csv' with the actual path to your CSV file
file_path = r'articles_raw\articles_raw.csv'

# Use the read_csv function to import the CSV file as a DataFrame
df = pd.read_csv(file_path, encoding="utf-8")

# Now 'df' is a Pandas DataFrame containing the data from the CSV file

df['Paragraph'] = df['Paragraph'].astype(str)
df['Zone'] = df['Zone'].astype(str)
df = df.drop_duplicates(subset='Headline')

print(df.shape)

sub_count = 30000

tf_count_max = 2000000

df_subset = df.iloc[:sub_count]

print("Zone_categories:",df_subset['Zone'].unique())

category_count_unique = df_subset['Zone'].nunique()

print("Zone_categories Count", category_count_unique)




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


cleaned_docs = clean_docs(paragraphs)


vectorizer = TfidfVectorizer(
    lowercase=True,
    max_features=tf_count_max,
    max_df=0.8,
    min_df=5,
    ngram_range=(1, 3),
    stop_words=None

)

vectors = vectorizer.fit_transform(cleaned_docs)

tfidf_array = vectors.toarray()




#print("df_shape",df["Paragraph"].iloc[:2])
#print("vectors",vectors.shape)
#print("tfidf_array", tfidf_array.shape)
#print("Vector for the first text:")
#for i, vector in enumerate(vectors):
#   print(f"Vector {i + 1}:")
#    print(vector)


print(tfidf_array)

tfidf_array_with_categories = pd.DataFrame(tfidf_array)

print(tfidf_array_with_categories.shape)


x = tfidf_array_with_categories

y = np.array(df_subset['Zone'])


print("X.shape = ", x.shape)
print("y.shape = ", y.shape)

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.3, random_state=0, shuffle=True)

print(len(x_train))
print(len(x_test))


# create list of model and accuracy dicts
perform_list = []


def run_model(model_name, est_c, est_pnlty):

    mdl=''

    if model_name == 'Logistic Regression':

        mdl = LogisticRegression()

    elif model_name == 'Random Forest':

      mdl = RandomForestClassifier(n_estimators=100 ,criterion='entropy' , random_state=0)

    elif model_name == 'Multinomial Naive Bayes':

     mdl = MultinomialNB(alpha=1.0,fit_prior=True)

    elif model_name == 'Support Vector Classifer':

      mdl = SVC()

    elif model_name == 'Decision Tree Classifier':

     mdl = DecisionTreeClassifier()

    elif model_name == 'K Nearest Neighbour':

        mdl = KNeighborsClassifier(n_neighbors=10 , metric= 'minkowski' , p = 4)

    elif model_name == 'Gaussian Naive Bayes':

     mdl = GaussianNB()

    oneVsRest = OneVsRestClassifier(mdl)

    oneVsRest.fit(x_train, y_train)

    y_pred = oneVsRest.predict(x_test)

    # Performance metrics

    accuracy = round(accuracy_score(y_test, y_pred) * 100, 2)

    # Get precision, recall, f1 scores

    precision, recall, f1score, support = score(y_test, y_pred, average='micro')

    print(f'Test Accuracy Score of Basic {model_name}: % {accuracy}')

    print(f'Precision : {precision}')

    print(f'Recall : {recall}')

    print(f'F1-score : {f1score}')

    # Add performance parameters to list

    perform_list.append(dict([

    ('Model', model_name),

    ('Test Accuracy', round(accuracy, 2)),

    ('Precision', round(precision, 2)),

    ('Recall', round(recall, 2)),

    ('F1', round(f1score, 2))

]))



run_model('Logistic Regression', est_c=None, est_pnlty=None)

run_model('Random Forest', est_c=None, est_pnlty=None)

run_model('Multinomial Naive Bayes', est_c=None, est_pnlty=None)

run_model('Support Vector Classifer', est_c=None, est_pnlty=None)

run_model('Decision Tree Classifier', est_c=None, est_pnlty=None)

run_model('K Nearest Neighbour', est_c=None, est_pnlty=None)

run_model('Gaussian Naive Bayes', est_c=None, est_pnlty=None)

model_performance = pd.DataFrame(data=perform_list)
model_performance = model_performance[['Model', 'Test Accuracy', 'Precision', 'Recall', 'F1']]
model = model_performance["Model"]
max_value = model_performance["Test Accuracy"].max()
print("The best accuracy of model is", max_value,"from Random")

model_performance.to_csv("model_data", index=False)

