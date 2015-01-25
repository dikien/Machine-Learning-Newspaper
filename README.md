Machine-Learning-Newspaper
======================

##**step1. data_wrangling.py**
- Get API Key from NYTimes.
- Get articles from NYTimes and convert json to csv format to save.
- They don't provide full article.
- Challenges:
 * simplejson library errors occurs and fixed it with upgrade 3.6.5.
 * Sometimes server timeout.
 * Article have utf-8 and unicode both of them.
 * Sometimes JSON Data contains journalist name but does not have article.
  
 
##**step2. data_exploratory.py**
- Clean stemmer with SnowballStemmer.
- Change encoding utf-8 to unicode.
- step2_data_exploratory.py generates pkl file with all article from 2010 to 2014.
 * It is to expensive to my MAC.
- step2_data_exploratory(2_people).py generates pkl file with two journalist's articles from 2010 to 2014.
 * It is not that expensive.
 * I choose two journalist, NEIL GENZLINGER and STEPHEN HOLDEN because they have written so many articles.
 
