# -*- coding: UTF-8 -*-
from __future__ import division
import os,re,string
from pymongo import Connection
from pymongo import ASCENDING #작은거부터
from pymongo import DESCENDING #큰거부터
import pymongo
from collections import Counter
import chardet
import re

connection = Connection('localhost', 27017)
db = connection.newspaper
#collection = db.hani

stopwords = """있다 있는 말했다 기자 것으로 대한 서울 밝혔다 한다 지난 이라고 했다 위해 대해 것은 것이다 등을 이날 통해 관련 그는 하는 함께 연합뉴스 없다 지난해 오전 그러나 위한
                  따라 이런 가운데 같은 다른 것이 부터 이번 하고 때문에 경우 오후 것을 하지만 가장 모두 까지 으로 최근 관계자는 에서 없는 이에 이후 특히 현재 이라며 등의 우리 아니라
                  라고 다시 한겨례 이를 이미지 이어 등이 당시 한국 관련기사 올해 많은 있다는 동안 뉴스리스트 사진 않고 이상 보면 않는 모든 국내 때문이다 보인다 많이 있는 원을 어떤 있을
                  원을 어떤 있을 라는 있었다 일부 한편 의원은 자신의 교수 그런 있다고 어떻게 직접 보고 않았다 등에 받은 이미 받고 새로운 아니다 됐다 크게 면서 각각 예정이다 않는 설명했다
                  정부가 것도 이는 있고 대표 지난날 그리고 결과 등으로 따르면 오는 만큼 알려졌다 없이 문제가 나는 관련해 세계 있지만 있도록 그의 앞으로 높은 문제를 다양한 주장했다 정부는 앞서
                  가능성이 갖고 하지 이라는 따른 덧붙였다 정부의 좋은 에는 물론 주요 여러 수도 지역 청와대 한다는 전했다 의원 이렇게 이들은 되는 같다 씨는 과정에서 교수는 만에 그동안
                  역시 전체 결국 라며 않을 않는다 들어 대상으로 전국 후보 않다 바로 계획이다 아닌 어느 너무 내년 또는 제대로 나타났다 강조했다 반면 열어 인기기사 더욱 계속 대해서는 대표는 아직
                  이들 사실을 먼저 지적했다 말을 지금 두고 또한 점을 해야 못한 내용을 비해 보다 일이 있습니다 관한 각종 등은 거의 정도 최대 하면 실제 처음 중요한 없었다 영향을 거쳐 쪽은
                  놓고 그런데 안에 사건 사회적 만든 원으로 기존 이제 일을 있던 대신 제공 우리는 매우 그가 중심으로 잇기 의견을 보는 수밖에 스스로 원의
                  앞에서 오히려 명이 전혀 정도로 방안을 이다 많다 입장을 것이라는 """

#test = {'$set' : {"kekeke" : "kekeke"}}
#print db.collection_names()
'''
for founds in collection.find():
    collection.update(founds, test, upsert=False, multi=True) # upsert, multi

for founds in collection.find():
    print founds
'''

''' update multi filed
for founds in collection.find():
    for key in founds.keys():
        if key == "article_number":
            year = founds[key][:4]
            month = founds[key][4:6]
            collection.update(founds, {'$set' : {"article_year" : year}}, upsert=False, multi=True)
            collection.update(founds, {'$set' : {"article_month" : month}}, upsert=False, multi=True)
'''
'''
for founds in collection.find({'article_indate' : {'$gte' : "20120101", '$lte' : "20120105"}, 'article_type' : 'politics'}).sort([("article_indate", ASCENDING)]).limit(5):
    print founds['article_indate']
    print founds['article_content']
'''

'''
# add indate field 
for founds in collection.find():
    year = founds['article_year']
    month = founds['article_month']
    day = founds['article_day']
    indate = year + month + day
    collection.update(founds, {'$set' : {"article_indate" : indate}}, upsert=False, multi=False)
'''

'''
for founds in collection.find():
     collection.update(founds, {'$set' : {"article_type" : "politics"}}, upsert=False, multi=False)
'''

#making index
#print collection.getIndexes();
#collection.create_index(["article_indate", ASCENDING], name="indate")
#collection.create_index(["article_type", ASCENDING], name="type")


'''
#중복값 제거(조선일보)
for founds in collection.find():
    for key in founds.keys():
        if key == "article_url":
            url = founds[key]
            if collection.find({'article_url' : url}).count() > 1:
                print founds["article_url"]
                collection.remove(founds)
'''
'''
#조선일보 article_type = politics 업데이트하기
for founds in collection.find():
     collection.update(founds, {'$set' : {"article_type" : "politics"}}, upsert=False, multi=False)
'''
'''
#중복값 제거(한겨례), 년도별로 하면 시간이 단축됨

for founds in collection.find({'article_year' : '2011'}):
    url = founds["article_url"]
    year = founds['article_year']
    month = founds['article_month']
    day = founds['article_day']
    type_1 = founds['article_type']
    if collection.find({'article_year' : year, 'article_month' : month, 'article_day' : day, 'article_type' : type_1, 'article_url' : url}).count() > 1:
                print year
                print founds["article_url"]
                collection.remove(founds)


                
for founds in collection.find({'article_year' : '2010'}):
    url = founds["article_url"]
    year = founds['article_year']
    month = founds['article_month']
    day = founds['article_day']
    type_1 = founds['article_type']
    if collection.find({'article_year' : year, 'article_month' : month, 'article_day' : day, 'article_type' : type_1, 'article_url' : url}).count() > 1:
                print year
                print founds["article_url"]
                collection.remove(founds)


                
for founds in collection.find({'article_year' : '2009'}):
    url = founds["article_url"]
    year = founds['article_year']
    month = founds['article_month']
    day = founds['article_day']
    type_1 = founds['article_type']
    if collection.find({'article_year' : year, 'article_month' : month, 'article_day' : day, 'article_type' : type_1, 'article_url' : url}).count() > 1:
                print year
                print founds["article_url"]
                collection.remove(founds)
'''

                
            


'''
for founds in collection.find({'article_year' : '2012', 'article_type' : 'culture', 'article_month' : '01'}):
    print founds['article_type'] + ' ' + founds['article_year'] + ' - ' + founds['article_month'] + ' '+ founds['article_day'] 
'''
                
                

'''5초걸림
for founds in collection.find():
    for key in founds.keys():
        if key == "article_number":
            day = founds[key][6:8]
            collection.update(founds, {'$set' : {"article_day" : day}}, upsert=False, multi=True)
'''
'''
for cline in range(0,40050,25):
    cline = str(cline)
    print "http://www.hani.co.kr/arti/politics/?type=1&cline=" + cline
'''
            
'''
for founds in collection.find({"article_year" : "2012"}): # db에 있는 내용 조회하는거
    for key in founds.keys():
        f = file('test.txt', 'w')
        content = str(founds) + "\n"
        f.write(content)
f.close()
'''
'''
#string안에서 그냥 검색하면 그 인물을 몇 회 인용했는지 나옴
a = "안철수 안철수가 안철수을
for word in re.findall(r"안철수",a):
    print word
'''
#Stop Word



'''
cnt = Counter() # 기사내용에서 단어 빈도 추출하는거
sum_article = []  
f = file('news_analysis_content.txt', 'w')
for founds in collection.find():
    for key in founds.keys():
        if key == "article_content":
            article_list = founds[key].split()
            for word in article_list:
                cnt[word] += 1

cnt_reverses = list(sorted(cnt, key=cnt.__getitem__, reverse=True))

for cnt_reverse in cnt_reverses:
    if len(cnt_reverse) != 1 and cnt[cnt_reverse] != 1:
        content = cnt_reverse + ":" + str(cnt[cnt_reverse]) + "\n"
        f.write(content)
f.close()


cnt = Counter()
sum_article = []  # 기사제목에서 단어 빈도 추출하는거
f = file('news_analysis_subject.txt', 'w')
for founds in collection.find({"article_year" : "2012", "article_month" : "09"}):
    for key in founds.keys():
        if key == "article_title":
            article_list = founds[key].split()
            for word in article_list:
                cnt[word] += 1

cnt_reverses = list(sorted(cnt, key=cnt.__getitem__, reverse=True))

for cnt_reverse in cnt_reverses:
    if len(cnt_reverse) != 1 and cnt[cnt_reverse] != 1:
        content = cnt_reverse + ":" + str(cnt[cnt_reverse]) + "\n"
        f.write(content)
f.close()
'''



#특정 단어가 기사에서 년월별로 몇번씩 사용되었는지 추출 
def frequency_period_content(year_start, year_end, w, types, where):
    if where == "hani":
        collection = db.hani
    if where == "chosun":
        collection = db.chosun
    if where == "donga":
        collection = db.donga
    if types != "all":
        cnt = {} # 기사내용에서 단어 빈도 추출하는거
        f = file(types + '_' + where + '_content' + "(" + str(year_start) + "-" + str(year_end) + ")" + '.txt', 'w')
        #f.write(str(year_start) + "부터 " + str(year_end) + "까지 " + types + "기사내용 " + w + "로 검색함" + "\n")
        goal = re.compile(w)
        #cnt = Counter()
        for founds in collection.find({'article_indate' : {'$gte' : year_start, '$lte' : year_end}, 'article_type' : types}, {"article_indate" : 1, "article_content" : 1}).sort([("article_indate", ASCENDING)]): #특정유형기사만 검색
            article_content = founds['article_content'].split()
            try:
                #if cnt[str(founds['article_indate'])[0:4] + '-' + str(founds['article_indate'])[4:6] + '-' + (founds['article_indate'])[6:8]] > 0: #일 
                if cnt[str(founds['article_indate'])[0:4] + '-' + str(founds['article_indate'])[4:6]] > 0: #월
                #if cnt[str(founds['article_indate'])[0:4]] > 0: #년
                    pass
            except:
                #cnt[str(founds['article_indate'])[0:4] + '-' + str(founds['article_indate'])[4:6] + '-' + (founds['article_indate'])[6:8]] = 0 #일
                cnt[str(founds['article_indate'])[0:4] + '-' + str(founds['article_indate'])[4:6]] = 0 #월
                #cnt[str(founds['article_indate'])[0:4]] = 0 #년
                #print "============================================================================="
            if len(article_content) != 0:
                for word in article_content:
                    if bool(goal.search(str(word))) is True:
                        #cnt[str(founds['article_indate'])[0:4] + '-' + str(founds['article_indate'])[4:6] + '-' + (founds['article_indate'])[6:8]] += 1 #일
                        cnt[str(founds['article_indate'])[0:4] + '-' + str(founds['article_indate'])[4:6]] += 1 #월
                        #cnt[str(founds['article_indate'])[0:4]] += 1 #년
        cnt_reverses = sorted(cnt.keys(), reverse=True) # cnt_reverses -> list
        for cnt_reverse in cnt_reverses:
            #content = cnt_reverse + " " + str(cnt[cnt_reverse]) + "\n"
            content = str(cnt[cnt_reverse]) + "\n"
            print content
            f.write(content)
        f.close()
        return "Successfully Extrated"
    else:
        cnt = {} # 기사내용에서 단어 빈도 추출하는거
        f = file(types + '_' + where + '_content' + "(" + str(year_start) + "-" + str(year_end) + ")" + '.txt', 'w')
        #f.write(str(year_start) + "부터 " + str(year_end) + "까지 " + types + "기사내용 " + w + "로 검색함" + "\n")
        goal = re.compile(w)
        #cnt = Counter()
        #for founds in collection.find({'article_indate' : {'$gte' : year_start, '$lte' : year_end}, 'article_type' : types}).sort([("article_indate", ASCENDING)]): #특정유형기사만 검색
        for founds in collection.find({'article_indate' : {'$gte' : year_start, '$lte' : year_end}}, {"article_indate" : 1, "article_content" : 1}).sort([("article_indate", ASCENDING)]): # 기사종류구분없이 검색 6초줄음
            article_content = founds['article_content'].split()
            try:
                #if cnt[str(founds['article_indate'])[0:4] + '-' + str(founds['article_indate'])[4:6] + '-' + (founds['article_indate'])[6:8]] > 0: #일 
                if cnt[str(founds['article_indate'])[0:4] + '-' + str(founds['article_indate'])[4:6]] > 0: #월
                #if cnt[str(founds['article_indate'])[0:4]] > 0: #년
                    pass
            except:
                #cnt[str(founds['article_indate'])[0:4] + '-' + str(founds['article_indate'])[4:6] + '-' + (founds['article_indate'])[6:8]] = 0 #일
                cnt[str(founds['article_indate'])[0:4] + '-' + str(founds['article_indate'])[4:6]] = 0 #월
                #cnt[str(founds['article_indate'])[0:4]] = 0 #년
                #print "============================================================================="
            if len(article_content) != 0:
                for word in article_content:
                    if bool(goal.search(str(word))) is True:
                        #cnt[str(founds['article_indate'])[0:4] + '-' + str(founds['article_indate'])[4:6] + '-' + (founds['article_indate'])[6:8]] += 1 #일
                        cnt[str(founds['article_indate'])[0:4] + '-' + str(founds['article_indate'])[4:6]] += 1 #월
                        #cnt[str(founds['article_indate'])[0:4]] += 1 #년
        cnt_reverses = sorted(cnt.keys(), reverse=True) # cnt_reverses -> list
        for cnt_reverse in cnt_reverses:
            #content = cnt_reverse + " " + str(cnt[cnt_reverse]) + "\n"
            content = str(cnt[cnt_reverse]) + "\n"
            print content
            f.write(content)
        f.close()
        return "Successfully Extrated"       


print frequency_period_content("20100101", "20120931", "해킹", "all", "donga")



#특정 단어가 기사제목에서 년월별로 몇번씩 사용되었는지 추출 
def frequency_period_title(year_start, year_end, w, types, where):
    if where == "hani":
        collection = db.hani
    if where == "chosun":
        collection = db.chosun
    cnt = {} # 기사내용에서 단어 빈도 추출하는거
    f = file(types + '_' + where + '_title' + "(" + str(year_start) + "-" + str(year_end) + ")" + '.txt', 'w')
    #f.write(str(year_start) + "부터 " + str(year_end) + "까지 " + types + "기사제목 " + w + "로 검색함" + "\n")
    goal = re.compile(w)
    #cnt = Counter()
    for founds in collection.find({'article_indate' : {'$gte' : year_start, '$lte' : year_end}, 'article_type' : types}, {"article_indate" : 1, "article_content" : 1}).sort([("article_indate", ASCENDING)]):
        article_content = founds['article_title'].split()
        try:
            if cnt[str(founds['article_indate'])[0:4] + '-' + str(founds['article_indate'])[4:6]] > 0:
                pass
        except:
            cnt[str(founds['article_indate'])[0:4] + '-' + str(founds['article_indate'])[4:6]] = 0
            #print "============================================================================="
        if len(article_content) != 0:
            for word in article_content:
                if bool(goal.search(str(word))) is True:
                    #cnt[(founds['article_indate'])[0:4] + '-' + (founds['article_indate'])[4:6] + '-' + (founds['article_indate'])[6:8]] += 1
                    cnt[(founds['article_indate'])[0:4] + '-' + (founds['article_indate'])[4:6]] += 1
    cnt_reverses = sorted(cnt.keys(), reverse=True) # cnt_reverses -> list
    for cnt_reverse in cnt_reverses:
        #content = cnt_reverse + " " + str(cnt[cnt_reverse]) + "\n"
        content = str(cnt[cnt_reverse]) + "\n"
        print content
        f.write(content)
    f.close()
    return "Successfully Extrated"

#print frequency_period_title("20060101", "20120930", "안철수", "politics", "한겨례신문")


def frequency_period_trend_title(year_start, year_end, types, where):
    if where == "hani":
        collection = db.hani
    if where == "chosun":
        collection = db.chosun
    cnt = Counter()
    sum_article = []  # 기사제목에서 단어 빈도 추출하는거
    f = file('frequency_period_trend_title' + '_' + types + '_' + where + "(" + str(year_start) + "-" + str(year_end) + ")" + '.txt', 'w')
    for founds in collection.find({'article_indate' : {'$gte' : year_start, '$lte' : year_end}, 'article_type' : types}, {"article_indate" : 1, "article_title" : 1}).sort([("article_indate", ASCENDING)]):
        article_list = founds["article_title"].split()
        for word in article_list:
            cnt[word] += 1
    cnt_reverses = list(sorted(cnt, key=cnt.__getitem__, reverse=True))
    for cnt_reverse in cnt_reverses:
    #if len(cnt_reverse) != 1 and cnt[cnt_reverse] != 1:
        content = cnt_reverse + ":" + str(cnt[cnt_reverse]) + "\n"
        f.write(content)
    f.close()

#print frequency_period_trend_title("20050101", "20051231", "culture", "hani")

    


'''
f = file('test1.txt', 'w') # read mode #파일 읽는거
f.write("abcde")
f.close()
'''
