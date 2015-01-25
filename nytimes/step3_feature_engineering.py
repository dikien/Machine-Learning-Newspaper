# -*- coding: UTF-8 -*-

import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer, TfidfVectorizer
from sklearn import preprocessing
from time import time
from sklearn import cross_validation
from sklearn.feature_selection import SelectPercentile, f_classif

def preprocess_4(article_file, lable_file):
    # article_file = "pkl/2013_article.pkl"
    # lable_file = "pkl/2013_lable.pkl"

    features = pickle.load(open(article_file))
    features = np.array(features)

    # transform non-numerical labels (as long as they are hashable and comparable) to numerical labels
    lables = pickle.load(open(lable_file))
    le = preprocessing.LabelEncoder()
    le.fit(lables)
    lables = le.transform(lables)

    ### test_size is the percentage of events assigned to the test set (remainder go into training)
    features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(features, lables, test_size=0.1, random_state=42)

    # print features_train.shape
    # print features_test[0]
    # print features_test.shape


    ### text vectorization--go from strings to lists of numbers
    t0 = time()
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, min_df=1,
                                 stop_words='english')
    features_train_transformed = vectorizer.fit_transform(features_train)
    features_test_transformed  = vectorizer.transform(features_test)

    # print "features_train_transformed is {}".format(features_train_transformed.shape)
    # print "features_test_transformed is {}".format(features_test_transformed.shape)
    # print "vectorizer time:", round(time()-t0, 3), "s"
    # print len(vectorizer.get_feature_names())

    ### feature selection, because text is super high dimensional and
    ### can be really computationally chewy as a result
    t0 = time()
    selector = SelectPercentile(f_classif, percentile=30)
    selector.fit(features_train_transformed, labels_train)
    features_train_transformed = selector.transform(features_train_transformed).toarray()
    features_test_transformed  = selector.transform(features_test_transformed).toarray()

    # print "features_train_transformed is {}".format(features_train_transformed.shape)
    # print "features_test_transformed is {}".format(features_test_transformed.shape)
    # print "selector time:", round(time()-t0, 3), "s"

    # print len(vectorizer.get_feature_names())
    # print vectorizer.get_feature_names()[0:-10]
    # print len(selector.scores_)

    return features_train_transformed, features_test_transformed, labels_train, labels_test

def preprocess_2(article_file, lable_file):
    # article_file = "pkl/2013_article.pkl"
    # lable_file = "pkl/2013_lable.pkl"

    features = pickle.load(open(article_file))
    features = np.array(features)

    # transform non-numerical labels (as long as they are hashable and comparable) to numerical labels
    lables = pickle.load(open(lable_file))
    le = preprocessing.LabelEncoder()
    le.fit(lables)
    lables = le.transform(lables)
    # print le.inverse_transform([0])

    ### text vectorization--go from strings to lists of numbers
    t0 = time()
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, min_df=1,
                                 stop_words='english')
    features_train_transformed = vectorizer.fit_transform(features)

    t0 = time()
    selector = SelectPercentile(f_classif, percentile=30)
    selector.fit(features_train_transformed, lables)
    features_train_transformed = selector.transform(features_train_transformed).toarray()

    return features_train_transformed, lables, vectorizer, selector, le


