# -*- coding: UTF-8 -*-

from time import time
from step3_feature_engineering import preprocess_2
from sklearn.svm import SVC
from sklearn.cross_validation import cross_val_score, KFold
from sklearn import grid_search

features, labels, vectorizer, selector, le = preprocess_2("pkl/article_2_people.pkl", "pkl/lable_2_people.pkl")

# Constructing the k-fold cross validation iterator (k=5)
cv = KFold(n=features.shape[0],  # total number of samples
           n_folds=10,           # number of folds the dataset is divided into
           shuffle=True,
           random_state=123)

t0 = time()

parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10, 100, 1000]}
clf = grid_search.GridSearchCV(SVC(), parameters)
clf.fit(features, labels)

# print cross_val_score(clf, features, labels, cv=cv, scoring='accuracy')
print "escape time : ", round(time()-t0, 3), "s"

print "best score is %s" % clf.best_score_
print "best parameter is %s" % clf.best_params_
print clf.grid_scores_


'''
escape time :  365.156 s
best score is 0.839794303797
best parameter is {'kernel': 'linear', 'C': 1}
[mean: 0.83979, std: 0.01271, params: {'kernel': 'linear', 'C': 1}, mean: 0.52097, std: 0.00029, params: {'kernel': 'rbf', 'C': 1}, mean: 0.81487, std: 0.02442, params: {'kernel': 'linear', 'C': 10}, mean: 0.52097, std: 0.00029, params: {'kernel': 'rbf', 'C': 10}, mean: 0.76622, std: 0.01725, params: {'kernel': 'linear', 'C': 100}, mean: 0.52136, std: 0.00048, params: {'kernel': 'rbf', 'C': 100}, mean: 0.73299, std: 0.00730, params: {'kernel': 'linear', 'C': 1000}, mean: 0.83900, std: 0.01419, params: {'kernel': 'rbf', 'C': 1000}]
'''





'''
# unit version
from time import time
from step3_vectorize_text import preprocess
from sklearn.svm import SVC
import numpy as np
from sklearn.metrics import accuracy_score
import collections

features_train, features_test, labels_train, labels_test = preprocess()


t0 = time()

clf = SVC(kernel='rbf', C=10000.0)
clf.fit(features_train, labels_train)

print "training time:", round(time()-t0, 3), "s"

t0 = time()

y_pred = clf.predict(features_test)

print "predicting time:", round(time()-t0, 3), "s"
print accuracy_score(labels_test, y_pred, normalize=True)

counter=collections.Counter(y_pred)
print counter

#########################################################

'''
