#!/usr/bin/env python
#
# file: nytimes_api_demo.py
#
# description: demonstrates basic interaction with the nytimes
#   newswire api to pull recent content posted to nytimes.com.
#   see also http://prototype.nytimes.com/gst/apitool/index.html
#   to play with this and other nytimes functionality.
#
# usage: ./nytimes_api_demo.py API_KEY
#
# requires: python 2.6 or later
#
# author: jake hofman (gmail: jhofman)
#

# import modules
import sys  # gives access to command line arguments in sys.argv
from urllib2 import urlopen  # for accessing urls
import json  # for parsing json strings to objects

RECENT_URL='http://api.nytimes.com/svc/news/v2/all/recent.json?api-key='

def print_recent(api_key):
    # construct the url by appending api key
    url=RECENT_URL+api_key

    # contact the nytimes api server and read result
    response=urlopen(url).read()

    # parse the resulting json string to an object 
    # 'result' is now an easily accessible dictionary
    result=json.loads(response)

    # get array of articles, returned in the 'results' field
    articles=result['results']

    # loop over articles, printing some article info
    for article in articles:        
        print article['section']
        print article['headline']
        print article['byline']
        print article['summary']
        print 

if __name__=='__main__':

    # check number of arguments provided
    if len(sys.argv) > 1:
        # first argument is api key
        api_key=sys.argv[1]

        print_recent(api_key)
    else:
        # show help
        print "usage: nytimes_api_demo.py API_KEY"
        print
        print "newswire api key required, available at at http://developer.nytimes.com/apps/register"
