# -*- coding: UTF-8 -*-
from __future__ import division
import os,copy,re,timeit,math,itertools,time,string,cProfile
import cookielib
from bs4 import BeautifulSoup
import chardet
import HTMLParser
import mechanize
from string import punctuation
import datetime, time
import urlparse
from pymongo import Connection


html_parser = HTMLParser.HTMLParser()

connection = Connection('localhost', 27017)
db = connection.newspaper
collection = db.chosun # collection = Table
#collection.insert({"a":3, "b":5})
'''
print db.collection_names()
for founds in collection.find(): # db에 있는 내용 조회하는거
    for key in founds.keys():
        if type(founds[key]) == unicode:
            print key,  " is ", founds[key]
        if type(founds[key]) == list:
            print key,  " is ", " ".join(founds[key])
'''     

# 1. 조선일보 (2006년 1월 1일 부터 가능함)
#http://news.chosun.com/svc/list_in/list.html?catid=2&indate=20120921&source=1&pn=1 source는 연합뉴스를 제외하는걸 의미함, indate는 그날의 뉴스를 검색하는거고 pn은 페이지를 의미함
#http://news.chosun.com/site/data/html_dir/2012/09/24/2012092400229.html
#http://m100.chosun.com/svc/guest//list.html?article=2012092400229&pn=1   pn은 댓글페이지를 의미함

def get_page(url): # 특정페이지를 출력(한글로변환)
    br = mechanize.Browser()
    br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1')]
    cj = cookielib.LWPCookieJar()
    br.set_handle_equiv(True)
    #br.set_handle_gzip(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    #response = br.open("http://news.chosun.com/svc/list_in/list.html?catid=2&indate=20120921&source=1&pn=1")
    response = br.open(url)
    contents = response.read()
    headers = response.info()
    if chardet.detect(contents)['encoding']:
        contents = unicode(contents, 'euc-kr').encode('utf-8')
        return html_parser.unescape(contents), headers
    
'''
def get_articles(url): # 2011.01.01 ~ 2012.09.30 
    data, headers = get_page(url)
    soup = BeautifulSoup(data)
    soup.prettify()
    #기자 
    content = soup('p')
    writer = str(content[0])
    writer = re.findall(r"Writer..........",writer)
    if len(writer) > 0:
        writer = writer[0][7:] # 기자 이름
    else:
        writer = "기자이름없음"
    #print "기자: " + writer
    #기사내용    
    content = soup.findAll("div", { "class" : "par" })
    tmp = []
    for i in range(len(content)):
        tmp.append(''.join([e for e in content[i].recursiveChildGenerator() if isinstance(e,unicode)]))
        tmp[i] = re.sub('[a-zA-Z]+|[0-9]+.|\s+',' ',tmp[i])
        for p in list(punctuation):
            tmp[i] = tmp[i].replace(p,' ')
            tmp[i] = tmp[i].replace("기사",'').replace("본문",'').replace("유형별",'').replace("포토",'').replace("팝업",'').replace("탭",'').replace("조선닷컴",'').replace("프로모션",'')
            tmp[i] = tmp[i].strip()
            tmp[i] = re.sub('  ',' ',tmp[i])
    content = "".join(tmp)
    # 입력, 수정시간
    dates = soup('p', id="date_text")
    dates = ''.join(dates[0].findAll(text=True))
    data_revise = []
    if dates.find("|") != -1: # 입력, 수정시간 둘다 있는 경우
        dates = dates.split("|")
        date_input = re.findall(r"20..............",dates[0])
        date_input_1 = str(date_input[0]) # data_input을 list에서 string으로 바꿔줌
        data_revise = re.findall(r"20..............",dates[1])
        date_revise_1 = str(data_revise[0]) # data_revise을 list에서 string으로 바꿔줌
        return writer, content, str(len(content)), date_input_1, date_revise_1
        #print "기사입력시간: " + date_input[0]
        #print "기사 마지막 수정시간: " + data_revise[0]
    else:
        date_input = re.findall(r"20..............",dates)
        date_input_1 = str(date_input[0])
        date_revise_1 = ""
        #print "기사입력시간: " + date_input[0]
        return writer, content, str(len(content)), date_input_1, date_revise_1
'''
'''   
def get_articles(url): # 2006.01.01 ~ 2006.12.31
    data, headers = get_page(url)
    soup = BeautifulSoup(data)
    soup.prettify()   
    content = soup.findAll("ul", { "class" : "article" })
    tmp = []
    for i in range(len(content)):
        tmp.append(''.join([e for e in content[i].recursiveChildGenerator() if isinstance(e,unicode)]))
        tmp[i] = re.sub('[a-zA-Z]+|[0-9]+.|\s+',' ',tmp[i])
        for p in list(punctuation):
            tmp[i] = tmp[i].replace(p,' ')
            tmp[i] = tmp[i].replace("기사",'').replace("본문",'').replace("유형별",'').replace("포토",'').replace("팝업",'').replace("탭",'').replace("조선닷컴",'').replace("프로모션",'')
            tmp[i] = tmp[i].strip()
            tmp[i] = re.sub('  ',' ',tmp[i])
    content = "".join(tmp)
    return content, str(len(content))
'''
'''
def get_articles(url): # 2007.01.01 ~ 2009.01.02
    data, headers = get_page(url)
    soup = BeautifulSoup(data)
    soup.prettify()   
    content = soup.findAll("div", { "id" : "Article" })
    tmp = []
    for i in range(len(content)):
        tmp.append(''.join([e for e in content[i].recursiveChildGenerator() if isinstance(e,unicode)]))
        tmp[i] = re.sub('[a-zA-Z]+|[0-9]+.|\s+',' ',tmp[i])
        for p in list(punctuation):
            tmp[i] = tmp[i].replace(p,' ')
            tmp[i] = tmp[i].replace("기사",'').replace("본문",'').replace("유형별",'').replace("포토",'').replace("팝업",'').replace("탭",'').replace("조선닷컴",'').replace("프로모션",'')
            tmp[i] = tmp[i].strip()
            tmp[i] = re.sub('  ',' ',tmp[i])
    content = "".join(tmp)
    return content, str(len(content))    
'''

def get_articles(url): # 2009.01.03 ~ 2010.12.31
    data, headers = get_page(url)
    soup = BeautifulSoup(data)
    soup.prettify()   
    content = soup.findAll("div", { "id" : "article" })
    tmp = []
    for i in range(len(content)):
        tmp.append(''.join([e for e in content[i].recursiveChildGenerator() if isinstance(e,unicode)]))
        tmp[i] = re.sub('[a-zA-Z]+|[0-9]+.|\s+',' ',tmp[i])
        for p in list(punctuation):
            tmp[i] = tmp[i].replace(p,' ')
            tmp[i] = tmp[i].replace("기사",'').replace("본문",'').replace("유형별",'').replace("포토",'').replace("팝업",'').replace("탭",'').replace("조선닷컴",'').replace("프로모션",'')
            tmp[i] = tmp[i].strip()
            tmp[i] = re.sub('  ',' ',tmp[i])
    content = "".join(tmp)
    return content, str(len(content)) 

#print get_articles("http://news.chosun.com/site/data/html_dir/2010/12/31/2010123100105.html")[0]

def get_comments(url):
    comments_body = get_page(url)[0]
    soup = BeautifulSoup(comments_body)
    soup.prettify()
    parsed = urlparse.urlparse(url)
    scheme, netloc, path, params, query, fragment = urlparse.urlparse(url)
    article_number = urlparse.parse_qs(parsed.query)['article'][0]
    #scheme + "://" + netloc + path + "?article=" + article_number + "&pn=" + page_number
    comments = soup.findAll("div", { "class" : "comment_txt" })
    comments_times = soup.findAll("p", { "class" : "user_data" })
    comments_ids = soup.findAll("li", { "class" : "user_ni" }) 
    comments_numbers = soup.findAll("li", { "id" : "art_tab2" })
    comments_votes = soup.findAll("p", { "class" : "user_etc" })
    print "==============="
    comments_number = comments_numbers[0].find('span').contents[0][1]
    for comment in comments:
        print comment.contents[0]
    for comment_time in comments_times:
        print comment_time.find('span').contents[0]
    for comments_id in comments_ids:
        print comments_id.find("a", { "class" : "u_name" }).contents[0]
        url = comments_id.find("a", { "class" : "u_name" })['href']
        parsed = urlparse.urlparse(url)
        print urlparse.parse_qs(parsed.query)['usr_id'][0]
    for comments_vote in comments_votes:
        agree =  comments_vote.findAll("a")[1].contents[0] #찬성
        disagree = comments_vote.findAll("a")[2].contents[0] #반대
        print re.findall(r"[0-9]+",agree)
        print re.findall(r"[0-9]+",disagree)
    '''
    if comments_number > 10:
        page_numbers = (comments_number % 10) + 2
        for page_number in range(2, page_number, 1):
    '''        
    
#get_comments("http://m100.chosun.com/svc/guest//list.html?article=2010070600127&pn=1")


def get_urls(url):
    data, headers = get_page(url) 
    soup = BeautifulSoup(data)
    soup.prettify()
    links = {}
    for link in soup.findAll('a', href = re.compile(r"site/data")):
        if len(link.contents) > 0:
            if (link.contents[0].find('img') != None):
                title = link.contents[0] #기사제목
                url = "http://news.chosun.com" + link['href'] #기사 URL
                links[url] = title
    
    if len(links) != 0:
        for link in links.keys():
            for p in list(punctuation): #기사 제목에 특수문자 제거
                links[link] = links[link].replace(p,' ')
                links[link] = links[link].strip()
                links[link] = re.sub('  ',' ',links[link])
                links[link] = "".join(links[link])
            #print links[link]
            #links[link] = links[link].split() # 기사 제목
            #print link # 기사 URL
            article_number = link.split("/")[-1][:-5] # 기사 고유번호(comments parsing시 사용)
            final_content, final_content_length = get_articles(link) # 기사내용, 기사길이
            '''
            print article_number
            print final_content
            print final_content_length
            '''
            print article_number[:8]
            collection.save({"article_title" : links[link],
                             "article_number" : article_number,
                             "article_url" : link,
                             "article_content" : final_content,
                             "article_length" : final_content_length})
            
            
            
#collection.insert({"a":3, "b":5})             
#get_urls("http://news.chosun.com/svc/list_in/list.html?catid=2&source=1&indate=20120602&pn=2")
        

date_end = datetime.date(2010, int('12'), 31)
date_start = datetime.date(2010, int('11'), int('10'))
one_day = datetime.timedelta(days=1)
tomorrow = date_start + one_day
diff = str(date_end - date_start).find("days")    
for i in range(int(str(date_end - date_start)[:diff])+1): #날짜의 차이 계산
    if i == 0:
        indate = str(date_start).replace("-","")
        print get_urls("http://news.chosun.com/svc/list_in/list.html?catid=2&indate=" + indate + "&source=1&pn=1")
        print get_urls("http://news.chosun.com/svc/list_in/list.html?catid=2&indate=" + indate + "&source=1&pn=2")
        print get_urls("http://news.chosun.com/svc/list_in/list.html?catid=2&indate=" + indate + "&source=1&pn=3")
    else:
        date_start = date_start + one_day
        indate = str(date_start).replace("-","")
        print get_urls("http://news.chosun.com/svc/list_in/list.html?catid=2&indate=" + indate + "&source=1&pn=1")
        print get_urls("http://news.chosun.com/svc/list_in/list.html?catid=2&indate=" + indate + "&source=1&pn=2")
        print get_urls("http://news.chosun.com/svc/list_in/list.html?catid=2&indate=" + indate + "&source=1&pn=3")


    

'''
#contents =  soup('p')
        #tmp[i] =  tmp[i].replace('\n','').replace('\t','') #태크 없애는 거임
#print contents
    tmp1 = ''.join([e for e in content[0].recursiveChildGenerator() if isinstance(e,unicode)])
    tmp1 =  tmp1.replace('\n','').replace('\t','') #태크 없애는 거임
    for p in list(punctuation):
        tmp1 = tmp1.replace(p,'')
    print tmp1
'''