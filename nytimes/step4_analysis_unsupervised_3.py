# -*- coding: UTF-8 -*-

from sklearn.metrics import accuracy_score
from time import time
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import preprocessing
from sklearn.feature_selection import SelectPercentile, f_classif, chi2
import matplotlib.pyplot as plt
from itertools import cycle
from sklearn.cluster import KMeans, SpectralClustering, AgglomerativeClustering
from sklearn.metrics import accuracy_score

def plot(data):
    colors = cycle('rgbcmykw')
    algorithm = sorted(data)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    for c in zip(colors):
        ax.plot([0], data, label=j, color=c)
        ax.scatter([0], data, color=c)

    plt.xlabel("#-Features(SelectPercentile)")
    plt.ylabel("Accuracy")
    plt.title("Accuracy vs #-Features for different classifiers")
    # ax.set_xscale("log")
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.3,
                    box.width, box.height * 0.7])
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=3)

    plt.legend(loc=2)
    plt.show()


def preprocess(article_file, lable_file):

    features = pickle.load(open(article_file))
    features = np.array(features)

    # transform non-numerical labels (as long as they are hashable and comparable) to numerical labels
    lables = pickle.load(open(lable_file))
    le = preprocessing.LabelEncoder()
    le.fit(lables)
    lables = le.transform(lables)
    # print le.inverse_transform([0])

    ### text vectorization--go from strings to lists of numbers
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, min_df=1,
                                 stop_words='english')
    features_train_transformed = vectorizer.fit_transform(features)

    # selector : chi2
    selector = SelectPercentile(score_func=chi2)
    selector.fit(features_train_transformed, lables)

    features_train_transformed = selector.transform(features_train_transformed).toarray()

    return features_train_transformed, lables, vectorizer, selector, le, features


data = []

features, labels, vectorizer, selector, le, features_data = preprocess("pkl/article_2_people.pkl", "pkl/lable_2_people.pkl")

for name, clf in [
    # ('k_means', KMeans(n_clusters=2, n_init=5)),
    # ('SpectralClustering', SpectralClustering(n_clusters=2, n_init=5)),
    # ('AgglomerativeClustering_ward', AgglomerativeClustering(n_clusters=2, linkage='ward')),
    # ('AgglomerativeClustering_complete', AgglomerativeClustering(n_clusters=2, linkage='complete')),
    ('AgglomerativeClustering_average', AgglomerativeClustering(n_clusters=2, linkage='average'))
]:


    print "*" * 100
    print('Method: {}'.format(name))

    # Fit on the whole data:
    t0 = time()
    y_pred = clf.fit(features).labels_
    print "fit time:", round(time()-t0, 3), "s"

    score_accuracy = accuracy_score(y_pred, labels, normalize=True)
    print('accuracy score on training: {}'.format(score_accuracy))

    print "*"* 100

    data.append(score_accuracy)

print data
plot(data)