# -*- coding: UTF-8 -*-

from time import time
from step3_feature_engineering import preprocess_2
from sklearn.cross_validation import cross_val_score, KFold
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.preprocessing import StandardScaler
from sklearn.lda import LDA
from sklearn.decomposition import PCA
from sklearn import grid_search

features, labels, vectorizer, selector, le = preprocess_2("pkl/article_2_people.pkl", "pkl/lable_2_people.pkl")

# Constructing the k-fold cross validation iterator (k=5)
cv = KFold(n=features.shape[0],  # total number of samples
           n_folds=10,           # number of folds the dataset is divided into
           shuffle=True,
           random_state=123)

t0 = time()

parameters = {'alpha':[1, 10, 100]}
clf = grid_search.GridSearchCV(BernoulliNB(), parameters)
clf.fit(features, labels)
# print cross_val_score(clf, features, labels, cv=cv, scoring='accuracy')
print "part1 time:", round(time()-t0, 3), "s"

print "best estimator is %s" % clf.best_estimator_
print "best score is %s" % clf.best_score_
print "best parameter is %s" % clf.best_params_
print clf.grid_scores_
print "=" * 90

clf_GaussianNB = Pipeline(steps=[
    ('scaler', StandardScaler()),
    ('classification', GaussianNB())
    ])

clf_pca = Pipeline(steps=[
    ('scaler', StandardScaler()),
    ('reduce_dim', PCA(n_components=1)),
    ('classification', GaussianNB())
    ])

clf_lda = Pipeline(steps=[
    ('scaler', StandardScaler()),
    ('reduce_dim', LDA(n_components=2)),
    ('classification', GaussianNB())
    ])


t0 = time()

scores = [
    cross_val_score(clf, features, labels, cv=cv, scoring='accuracy')

            for clf in [clf_GaussianNB, clf_pca, clf_lda]
    ]

print "part2 time:", round(time()-t0, 3), "s"
print "GaussianNB score is %s" % round(scores[0].mean(), 5)
print "GaussianNB score at PCA(n_components=1) is %s" % round(scores[1].mean(), 5)
print "GaussianNB score at LDA(n_components=2) is %s" % round(scores[2].mean(), 5)

'''
part1 time: 1.055 s
best estimator is BernoulliNB(alpha=1, binarize=0.0, class_prior=None, fit_prior=True)
best score is 0.862737341772
best parameter is {'alpha': 1}
[mean: 0.86274, std: 0.01352, params: {'alpha': 1}, mean: 0.66653, std: 0.02254, params: {'alpha': 10}, mean: 0.52097, std: 0.00029, params: {'alpha': 100}]
==========================================================================================
part2 time: 255.563 s
GaussianNB score is 0.92088
GaussianNB score at PCA(n_components=1) is 0.53283
GaussianNB score at LDA(n_components=2) is 0.72351
'''



'''
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

t0 = time()

clf = GaussianNB()
clf.fit(features_train, labels_train)

print "training time:", round(time()-t0, 3), "s"

t0 = time()

y_pred = clf.predict(features_test)

print "predicting time:", round(time()-t0, 3), "s"
print accuracy_score(labels_test, y_pred, normalize=True)

# for i, j in enumerate(clf.feature_importances_):
#     if j >  0.1:
#         print (i, j)
#
# print max(clf.feature_importances_)
'''
###################################