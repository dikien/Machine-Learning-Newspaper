# -*- coding: UTF-8 -*-

from time import time
from step3_feature_engineering import preprocess_2
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import KFold
from sklearn import grid_search

features, labels, vectorizer, selector, le = preprocess_2("pkl/article_2_people.pkl", "pkl/lable_2_people.pkl")

# Constructing the k-fold cross validation iterator (k=5)
cv = KFold(n=features.shape[0],  # total number of samples
           n_folds=5,           # number of folds the dataset is divided into
           shuffle=True,
           random_state=123)

t0 = time()

parameters = {'algorithm':('ball_tree', 'kd_tree', 'brute'), 'n_neighbors':[5, 50, 500]}
clf = grid_search.GridSearchCV(KNeighborsClassifier(), parameters)
clf.fit(features, labels)

print "escape time : ", round(time()-t0, 3), "s"

print "best score is %s" % clf.best_score_
print "best parameter is %s" % clf.best_params_
print clf.grid_scores_

'''
escape time :  121.11 s
best score is 0.587025316456
best parameter is {'n_neighbors': 50, 'algorithm': 'ball_tree'}
[mean: 0.58386, std: 0.02612, params: {'n_neighbors': 5, 'algorithm': 'ball_tree'}, mean: 0.58703, std: 0.09922, params: {'n_neighbors': 50, 'algorithm': 'ball_tree'}, mean: 0.56448, std: 0.06137, params: {'n_neighbors': 500, 'algorithm': 'ball_tree'}, mean: 0.55380, std: 0.03316, params: {'n_neighbors': 5, 'algorithm': 'kd_tree'}, mean: 0.58703, std: 0.09922, params: {'n_neighbors': 50, 'algorithm': 'kd_tree'}, mean: 0.56448, std: 0.06137, params: {'n_neighbors': 500, 'algorithm': 'kd_tree'}, mean: 0.57120, std: 0.01555, params: {'n_neighbors': 5, 'algorithm': 'brute'}, mean: 0.58703, std: 0.09922, params: {'n_neighbors': 50, 'algorithm': 'brute'}, mean: 0.56448, std: 0.06137, params: {'n_neighbors': 500, 'algorithm': 'brute'}]
'''