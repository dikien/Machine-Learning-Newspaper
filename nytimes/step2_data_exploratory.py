# -*- coding: UTF-8 -*-

from collections import defaultdict
import operator
from glob import glob
from nltk.stem.snowball import SnowballStemmer
import pickle
from time import time

def make_pkl():

    data = []
    labels = []
    filelists = []

    filelists_2010 = glob("articles/2010/*.csv")
    filelists_2011 = glob("articles/2011/*.csv")
    filelists_2012 = glob("articles/2012/*.csv")
    filelists_2013 = glob("articles/2013/*.csv")
    filelists_2014 = glob("articles/2014/*.csv")

    print "there are %s articles at 2010" % len(filelists_2010)
    print "there are %s articles at 2011" % len(filelists_2011)
    print "there are %s articles at 2012" % len(filelists_2012)
    print "there are %s articles at 2013" % len(filelists_2013)
    print "there are %s articles at 2014" % len(filelists_2014)

    # save filelists to all filename list
    filelists.extend(filelists_2010)
    filelists.extend(filelists_2011)
    filelists.extend(filelists_2012)
    filelists.extend(filelists_2013)
    filelists.extend(filelists_2014)

    t0 = time()

    for file in filelists:
        with open(file) as ifile:
            for line in ifile:

                tokens = line.strip().split('\t')

                # tokens[0] : journalist name
                # tokens[1] : article
                # if there was no journalist name, get rid of them.
                if len(tokens) == 2 and \
                                tokens[0] != "THE EDITORIAL BOARD" and \
                                tokens[0] != "THE NEW YORK TIMES":

                    # stemmer
                    stemmer = SnowballStemmer("english", ignore_stopwords=True)

                    # change utf-8 to unicode
                    text_string = tokens[1].decode('utf-8','ignore').split()

                    # delete stemmer
                    words = [stemmer.stem(text) for text in text_string]
                    words = " ".join(words)

                    labels.append(tokens[0])
                    data.append(words)

    print "stemmer time:", round(time()-t0, 3), "s"

    journalist = defaultdict(int)

    t0 = time()

    for x in labels:
        journalist[x] += 1

    sorted_journalist = sorted(journalist.items(), key=operator.itemgetter(1))
    print "sorting time:", round(time()-t0, 3), "s"

    # the number of journalist in 2013 : 5140
    print "there are %s journalist" % len(journalist)

    t0 = time()

    pickle.dump(data, open("pkl/article.pkl", "w") )
    pickle.dump(labels, open("pkl/lable.pkl", "w") )
    print "pickle time:", round(time()-t0, 3), "s"

make_pkl()