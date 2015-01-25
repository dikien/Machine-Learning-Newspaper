# -*- coding: UTF-8 -*-

from time import time
from step3_feature_engineering import preprocess_2
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import KFold
from sklearn import grid_search

features, labels, vectorizer, selector, le = preprocess_2("pkl/article_2_people.pkl", "pkl/lable_2_people.pkl")

# Constructing the k-fold cross validation iterator (k=10)
cv = KFold(n=features.shape[0],  # total number of samples
           n_folds=10,           # number of folds the dataset is divided into
           shuffle=True,
           random_state=123)

t0 = time()

parameters = {'min_samples_split':[10, 50, 100, 1000]}
clf = grid_search.GridSearchCV(RandomForestClassifier(), parameters)
clf.fit(features, labels)

print "escape time : ", round(time()-t0, 3), "s"

print "best estimator is %s" % clf.best_estimator_
print "best score is %s" % clf.best_score_
print "best parameter is %s" % clf.best_params_
print clf.grid_scores_

'''
escape time :  7.764 s
best estimator is RandomForestClassifier(bootstrap=True, compute_importances=None,
            criterion='gini', max_depth=None, max_features='auto',
            max_leaf_nodes=None, min_density=None, min_samples_leaf=1,
            min_samples_split=10, n_estimators=10, n_jobs=1,
            oob_score=False, random_state=None, verbose=0)
best score is 0.759098101266
best parameter is {'min_samples_split': 10}
[mean: 0.75910, std: 0.01045, params: {'min_samples_split': 10}, mean: 0.75435, std: 0.00763, params: {'min_samples_split': 50}, mean: 0.75316, std: 0.02721, params: {'min_samples_split': 100}, mean: 0.62302, std: 0.02624, params: {'min_samples_split': 1000}]
'''