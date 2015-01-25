# -*- coding: UTF-8 -*-

import requests
import csv
import time
import sys

basic_url = "http://api.nytimes.com/svc/search/v2/articlesearch.json"

payload = {"api-key" : "input your api key",
           "callback" : "svc_search_v2_articlesearch",
           "sort" : "oldest",
           "fl" : "lead_paragraph,byline",
           "page" : "1"
}

def trans_json_to_csv(date):
    '''
    if data == 20101010 -> 20101010.csv will be saved with article that were written in 2010.10.10
    :param date: date
    :return: nothing
    '''
    ft = open("articles/"+ date + ".csv", "wb+")
    f = csv.writer(ft, delimiter='\t')
    payload.update({"begin_date" : date, "end_date" : date})
    docs_lens = 1
    page = 1

    while(docs_lens > 0 and page < 15):
        # when page get around 100, there were some errors.
        try:
            r = requests.get(basic_url, params=payload)
        except:
            r = requests.get(basic_url, params=payload)

        # If one day limie query occurs, exit(0)
        if "X-Mashery-Error-Code" in r.headers:
            print "ERR_403_DEVELOPER_OVER_RATE"
            sys.exit(0)

        try:
            contents = r.json()
            for k in contents["response"]["docs"]:
                # Don't save "THE ASSOCIATED PRESS" and "REUTERS" because these are not the goal of this.
                if type(k["byline"]) == dict \
                        and type(k["lead_paragraph"]) == unicode\
                        and k["byline"]["original"].replace("By ", "").encode("UTF-8", errors="ignore") != "THE ASSOCIATED PRESS"\
                        and k["byline"]["original"].replace("By ", "").encode("UTF-8", errors="ignore") != "REUTERS":
                    f.writerow([k["byline"]["original"].replace("By ", "").encode("UTF-8", errors="ignore"), # write "writer"
                                k["lead_paragraph"].encode("UTF-8", errors="ignore") # write "lead paragraph"
                                ])
                    print "writer is %s" % k["byline"]["original"].replace("By ", "")
            time.sleep(0.5)
                    # print "paragraph is %s" % k["lead_paragraph"]

            print "page number is %s" % page
            page += 1

            docs_lens = len(contents["response"]["docs"])
            print "doc length is %s" % docs_lens
            payload.update({"page" : page})

        except Exception as e:
            page += 1
            print "page number is %s" % page
            print e
            # print json.dumps(contents, indent=4, sort_keys=True)
            pass
    ft.close()


for month in range(1,13):
    if month < 10:
        month = str(month)
        month = "2010" + "0" + month
    else:
        month = str(month)
        month = "2010" + month

    for day in range(1, 32):
        if day < 10:
            day = str(day)
            day = "0" + day
            date = month + day
            print "%s is starting" % date
            trans_json_to_csv(date)
            print "%s is done" % date
        else:
            day = str(day)
            date = month + day
            print "%s is starting" % date
            trans_json_to_csv(date)
            print "%s is done" % date