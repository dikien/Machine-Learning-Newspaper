# -*- coding: UTF-8 -*-

from time import time
from step3_feature_engineering import preprocess_2
from sklearn.ensemble import AdaBoostClassifier
from sklearn.cross_validation import KFold
from sklearn import grid_search

features, labels, vectorizer, selector, le = preprocess_2("pkl/article_2_people.pkl", "pkl/lable_2_people.pkl")

# Constructing the k-fold cross validation iterator (k=10)
cv = KFold(n=features.shape[0],  # total number of samples
           n_folds=10,           # number of folds the dataset is divided into
           shuffle=True,
           random_state=123)

t0 = time()
parameters = {'algorithm':('SAMME.R', 'SAMME')}
clf = grid_search.GridSearchCV(AdaBoostClassifier(), parameters)
clf.fit(features, labels)

print "escape time : ", round(time()-t0, 3), "s"
print "best estimator is %s" % clf.best_estimator_
print "best score is %s" % clf.best_score_
print "best parameter is %s" % clf.best_params_
print clf.grid_scores_

'''
escape time :  41.558 s
best estimator is AdaBoostClassifier(algorithm='SAMME.R', base_estimator=None,
          learning_rate=1.0, n_estimators=50, random_state=None)
best score is 0.683148734177
best parameter is {'algorithm': 'SAMME.R'}
[mean: 0.68315, std: 0.01696, params: {'algorithm': 'SAMME.R'}, mean: 0.62144, std: 0.02704, params: {'algorithm': 'SAMME'}]
'''