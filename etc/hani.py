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
collection = db.hani # collection = Table

def get_page(url): # 특정페이지를 출력(한글로변환)
    br = mechanize.Browser()
    br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1')]
    cj = cookielib.LWPCookieJar()
    br.set_handle_equiv(True)
    #br.set_handle_gzip(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    response = br.open(url)
    contents = response.read()
    headers = response.info()
    return html_parser.unescape(contents)

    
def get_articles(url): # 2005.01.01 ~ 2012.10.03
    data = get_page(url)
    soup = BeautifulSoup(data)
    soup.prettify()
    content = soup.findAll("div", { "class" : "article-contents" })
    tmp = []
    for i in range(len(content)):
        tmp.append(''.join([e for e in content[i].recursiveChildGenerator() if isinstance(e,unicode)]))
        tmp[i] = re.sub('[a-zA-Z]+|[0-9]+.|\s+',' ',tmp[i])
        for p in list(punctuation):
            tmp[i] = tmp[i].replace(p,' ')
            tmp[i] = tmp[i].replace("“",' ').replace("”",' ').replace("·",' ').replace("△",' ').replace("■",' ').replace("‘",' ').replace("’",' ').replace("…",' ').replace("【서울 뉴시스】",' ').replace("▲",' ').replace("⊙",' ').replace("◇",' ').replace("▶",' ').replace("◆",' ').replace("【춘천 뉴시스】",' ')
            tmp[i] = tmp[i].strip()
            tmp[i] = re.sub('  ',' ',tmp[i])
    content = "".join(tmp)
    return content, str(len(content)) 


def get_urls(url):
    data = get_page(url) 
    soup = BeautifulSoup(data)
    soup.prettify()
    links = {}
    basic_url = "http://www.hani.co.kr"
    contents = soup.findAll("ul", { "class" : "subject-list" })
    for content in contents[0]:
        if str(content) != '\n':
            data1 = str(content)
            soup1 = BeautifulSoup(data1)
            for link in soup1.findAll('li'):
                url =  basic_url + str(link.contents[1]['href'])
                final_content = get_articles(url)[0] # 기사내용
                final_content_length = get_articles(url)[1] # 기사길이
                if len(link.contents[1].contents) != 0: # 기사제목이 없을때 에러방지
                    final_title = str(link.contents[1].contents[0]) 
                else:
                    final_title = ""
                for p in list(punctuation):
                    final_title = final_title.replace(p,' ')
                    final_title = final_title.replace("“",' ').replace("”",' ').replace("·",' ').replace("△",' ').replace("■",' ').replace("‘",' ').replace("’",' ').replace("…",' ').replace("▲",' ').replace("⊙",' ').replace("◇",' ').replace("▶",' ').replace("◆",' ')
                    final_title = final_title.strip()
                    final_title = re.sub('  ',' ',final_title)
                year = str(link.contents[3])[4:8] # year
                month = str(link.contents[3])[9:11] # month
                day = str(link.contents[3])[12:14] # day
                print year + "-" + month + "-" + day
                print final_title
                print final_content

                collection.save({"article_title" : final_title,
                                 "article_url" : url,
                                 "article_content" : final_content,
                                 "article_length" : final_content_length,
                                 "article_year" : year,
                                 "article_month" : month,
                                 "article_day" : day,
                                 "article_type" : "society"})


get_urls("http://www.hani.co.kr/arti/society/?type=1&cline=179")
