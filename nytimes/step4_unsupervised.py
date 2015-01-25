# -*- coding: UTF-8 -*-

from sklearn.cluster import KMeans, SpectralClustering, AgglomerativeClustering
from sklearn.metrics import accuracy_score
from time import time
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import preprocessing
from sklearn.feature_selection import SelectPercentile, f_classif, chi2
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.feature_selection import RFECV
from sklearn.svm import SVR
from sklearn import grid_search
from nltk.stem.snowball import SnowballStemmer
import scipy as sp
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel

def preprocess_2(article_file, lable_file):

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

    # selector : SelectPercentile
    # selector = SelectPercentile(f_classif, percentile=30)
    # selector.fit(features_train_transformed, lables)

    # selector : SelectKBest
    # selector = SelectKBest(k=100)
    # selector.fit(features_train_transformed, lables)

    # selector : RFECV takes some time
    # estimator = SVR(kernel="linear")
    # selector = RFECV(estimator, cv=2, step=1)
    # selector.fit(features_train_transformed, lables)

    # selector : chi2
    selector = SelectPercentile(score_func=chi2)
    selector.fit(features_train_transformed, lables)

    features_train_transformed = selector.transform(features_train_transformed).toarray()

    return features_train_transformed, lables, vectorizer, selector, le, features

features, labels, vectorizer, selector, le, features_data = preprocess_2("pkl/article_2_people.pkl", "pkl/lable_2_people.pkl")



estimators = {'k_means': KMeans(n_clusters=2, n_init=5),
              'SpectralClustering' : SpectralClustering(n_clusters=2, n_init=5),
              'AgglomerativeClustering_ward' : AgglomerativeClustering(n_clusters=2, linkage='ward'),
              'AgglomerativeClustering_complete' : AgglomerativeClustering(n_clusters=2, linkage='complete'),
              'AgglomerativeClustering_average' : AgglomerativeClustering(n_clusters=2, linkage='average'),
              }

for name, clf in estimators.items():

    t0 = time()
    y_pred = clf.fit(features).labels_
    print "estimator is %s" % name
    print "fit time:", round(time()-t0, 3), "s"
    print "accuracy_score : %s" % accuracy_score(labels, y_pred, normalize=True)
    print "=" * 90

'''
estimator is SpectralClustering
fit time: 2.318 s
accuracy_score : 0.592167721519

estimator is AgglomerativeClustering_complete
fit time: 16.317 s
accuracy_score : 0.500791139241

estimator is k_means
fit time: 0.066 s
accuracy_score : 0.411787974684

estimator is AgglomerativeClustering_average
fit time: 16.481 s
accuracy_score : 0.479825949367

estimator is AgglomerativeClustering_ward
fit time: 16.42 s
accuracy_score : 0.496439873418
'''


clf = KMeans(n_clusters=2, n_init=5)
clf.fit(features)

# s1 is NEIL GENZLINGER's article from http://www.nytimes.com/movies/movie/477894/Little-Hope-Was-Arson/overview
# Let's look at KMeans will predict s1 is his article.
s1 = "There’s nothing fancy about “Little Hope Was Arson,” a documentary on the 2010 church fires in East Texas, and that’s the beauty of it. The filmmaker, Theo Love, presents the people in the story as they are, without passing judgment and without apology, whether they are investigators or pastors or just ordinary folks caught up in the inexplicable. It’s Americana unvarnished and, because of that, as absorbing as it is respectful. — Neil Genzlinger"

features_test = []
stemmer = SnowballStemmer("english", ignore_stopwords=True)
text_string = s1.decode('utf-8','ignore').split()
words = [stemmer.stem(text) for text in text_string]
words = " ".join(words)
features_test.append(words)

print "After stemmer s1 : %s " %features_test
features_test = np.array(features_test)

new_post_vec = vectorizer.transform(features_test)
new_post_vec  = selector.transform(new_post_vec).toarray()
new_post_label = clf.predict(new_post_vec)

print new_post_label

similar = []
similar_indices = (clf.labels_ == new_post_label).nonzero()[0]

for i in similar_indices:
    dist = sp.linalg.norm((new_post_vec - features[i]))
    similar.append((dist, features_data[i]))

similar = sorted(similar)
print len(similar)

show_at_1 = similar[0]
show_at_2 = similar[len(similar)/2]
show_at_3 = similar[-1]

print "first : %s " %show_at_1[1]
print "middle : %s" %show_at_2[1]
print "last : %s " %show_at_3[1]

print "cosine scores ==> ",cosine_similarity(features[:,:], new_post_vec)  #here the first element of tfidf_matrix_train is matched with other three elements

test =  cosine_similarity(features[:,:], new_post_vec)
# print test.shape
print test[test > 0.33]
features_data = np.ravel(features_data)

features_data = features_data.reshape((2528,1))
# print features_data.shape
# print features_data[test > 0.33]

cosine_similarities = linear_kernel(features[:,:], new_post_vec).flatten()
related_docs_indices = cosine_similarities.argsort()[:-5:-1]
print related_docs_indices

# print np.count_nonzero(np.isposinf(test))
# print new_post_vec.shape.type
# ~sp.isnan(data[:,0])

'''
After stemmer s1 : [u'there noth fanci about \u201clittl hope was arson,\u201d a documentari on the 2010 church fire in east texas, and that the beauti of it. the filmmaker, theo love, present the peopl in the stori as they are, without pass judgment and without apology, whether they are investig or pastor or just ordinari folk caught up in the inexplicable. it americana unvarnish and, because of that, as absorb as it is respectful. \u2014 neil genzling']
[0]
2480
first : the drama “two lives,” with julian köhler and liv ullmann, focus on a happili marri woman and appar east german spi whose secret threaten to destroy her famili life.

middle : isabella rossellini talk about the sex live found in the natur world in “green porno,” at the brooklyn academi of music.

last : “megastorm” on the discoveri channel is among three show that examin hurrican sandy.
cosine scores ==>  [[ 0.        ]
 [ 0.        ]
 [ 0.        ]
 ...,
 [ 0.        ]
 [ 0.        ]
 [ 0.11783466]]
[ 0.44863413  0.3553121   0.39469066  0.3553121   0.33836096]
[1845 2318  707  589]
'''