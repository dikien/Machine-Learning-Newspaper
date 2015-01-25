# -*- coding: UTF-8 -*-

from __future__ import print_function
import numpy as np
from sklearn.cross_validation import KFold
from sklearn.linear_model import LinearRegression, ElasticNet, Lasso, Ridge, ElasticNetCV
from sklearn.metrics import mean_squared_error, r2_score
from step3_feature_engineering import preprocess_4
from time import time

features_train, features_test, labels_train, labels_test = preprocess_4("pkl/article_2_people.pkl", "pkl/lable_2_people.pkl")

x = np.concatenate([features_train, features_test])
y = np.concatenate([labels_train, labels_test])

for name, met in [
        ('linear regression', LinearRegression(fit_intercept=True)),
        ('lasso()', Lasso()),
        ('elastic-net(.5)', ElasticNet(alpha=0.5)),
        ('lasso(.5)', Lasso(alpha=0.5)),
        ('ridge(.5)', Ridge(alpha=0.5)),
]:
    # Fit on the whole data:
    t0 = time()
    met.fit(x, y)
    print ("training time:", round(time()-t0, 3), "s")

    # Predict on the whole data:
    t0 = time()
    p = met.predict(x)
    print ("predicting time:", round(time()-t0, 3), "s")
    r2_train = r2_score(y, p)

    # Now, we use 5 fold cross-validation to estimate generalization error
    kf = KFold(len(x), n_folds=5)
    p = np.zeros_like(y)
    for train, test in kf:
        met.fit(x[train], y[train])
        p[test] = met.predict(x[test])

    r2_cv = r2_score(y, p)
    print('Method: {}'.format(name))
    print('R2 on training: {}'.format(r2_train))
    print('R2 on 5-fold CV: {}'.format(r2_cv))
    print()


for name, met in [
        ('linear regression', LinearRegression()),
        ('lasso()', Lasso()),
        ('elastic-net(.5)', ElasticNet(alpha=0.5)),
        ('lasso(.5)', Lasso(alpha=0.5)),
        ('ridge(.5)', Ridge(alpha=0.5)),
]:
    # Fit on the whole data:
    t0 = time()
    met.fit(x, y)
    print ("training time:", round(time()-t0, 3), "s")

    # Predict on the whole data:
    t0 = time()
    p = met.predict(x)
    print ("predicting time:", round(time()-t0, 3), "s")
    r2_train = r2_score(y, p)

    # Now, we use 5 fold cross-validation to estimate generalization error
    kf = KFold(len(x), n_folds=5)
    p = np.zeros_like(y)
    for train, test in kf:
        met.fit(x[train], y[train])
        p[test] = met.predict(x[test])

    r2_cv = r2_score(y, p)
    print('Method: {}'.format(name))
    print('R2 on training: {}'.format(r2_train))
    print('R2 on 5-fold CV: {}'.format(r2_cv))
    print()

# Construct an ElasticNetCV object (use all available CPUs)
met = ElasticNetCV(n_jobs=-1, l1_ratio=[.01, .05, .25, .5, .75, .95, .99])

kf = KFold(len(x), n_folds=5)
pred = np.zeros_like(y)
for train, test in kf:
    met.fit(x[train], y[train])
    pred[test] = met.predict(x[test])


print('[EN CV l1_ratio] RMSE on testing (5 fold), {:.2}'.format(np.sqrt(mean_squared_error(y, p))))
print('[EN CV l1_ratio] R2 on testing (5 fold), {:.2}'.format(r2_score(y, p)))
print('')


'''
# unit version
from time import time
import numpy as np
from step3_vectorize_text import preprocess_4
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

features_train, features_test, labels_train, labels_test = preprocess_4("pkl/article_2_people.pkl", "pkl/lable_2_people.pkl")

t0 = time()

clf = LinearRegression()
clf.fit(features_train, labels_train)

print "training time:", round(time()-t0, 3), "s"

t0 = time()

y_pred = clf.predict(features_test)

print "predicting time:", round(time()-t0, 3), "s"

print clf.coef_
print clf.intercept_
print("RMSE: {:.2}.".format(np.sqrt(mean_squared_error(y_pred, labels_test))))
cod = r2_score(y_pred, labels_test)
print('COD (on training data): {:.2}'.format(cod))
'''