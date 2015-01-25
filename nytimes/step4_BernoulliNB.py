# -*- coding: UTF-8 -*-

from time import time
from step3_feature_engineering import preprocess_2
from sklearn.naive_bayes import BernoulliNB
from nltk.stem.snowball import SnowballStemmer
import numpy as np

features, labels, vectorizer, selector, le = preprocess_2("pkl/article_2_people.pkl", "pkl/lable_2_people.pkl")

t0 = time()
clf = BernoulliNB(alpha=1)
clf.fit(features, labels)
print "training time :", round(time()-t0, 3), "s"

t0 = time()
# s1 is NEIL GENZLINGER's article from http://www.nytimes.com/movies/movie/477894/Little-Hope-Was-Arson/overview
# Let's look at BernoulliNB will predict s1 is his article.
s1 = "There’s nothing fancy about “Little Hope Was Arson,” a documentary on the 2010 church fires in East Texas, and that’s the beauty of it. The filmmaker, Theo Love, presents the people in the story as they are, without passing judgment and without apology, whether they are investigators or pastors or just ordinary folks caught up in the inexplicable. It’s Americana unvarnished and, because of that, as absorbing as it is respectful. — Neil Genzlinger"

features_test = []
stemmer = SnowballStemmer("english", ignore_stopwords=True)
text_string = s1.decode('utf-8','ignore').split()
words = [stemmer.stem(text) for text in text_string]
words = " ".join(words)
features_test.append(words)

print "After stemmer s1 : %s " %features_test

features_test = np.array(features_test)
features_test_transformed  = vectorizer.transform(features_test)
features_test_transformed  = selector.transform(features_test_transformed).toarray()

y_pred = clf.predict(features_test_transformed)
print le.inverse_transform(y_pred)


'''
training time : 0.102 s
After stemmer s1 : [u'there noth fanci about \u201clittl hope was arson,\u201d a documentari on the 2010 church fire in east texas, and that the beauti of it. the filmmaker, theo love, present the peopl in the stori as they are, without pass judgment and without apology, whether they are investig or pastor or just ordinari folk caught up in the inexplicable. it americana unvarnish and, because of that, as absorb as it is respectful. \u2014 neil genzling']
['NEIL GENZLINGER']
'''