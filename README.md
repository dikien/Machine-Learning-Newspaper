Machine-Learning-Newspaper
======================

**step1. data_wrangling.py**
- Get API Key from NYTimes
- Get articles from NYTimes and convert json to csv format to save
- They don't provide full article
- Challenges:
  * simplejson library errors occurs and fixed it with upgrade 3.6.5
  * Sometimes server timeout
  * Article have utf-8 and unicode both of them
  * Sometimes JSON Data contains journalist name but does not have article!
  