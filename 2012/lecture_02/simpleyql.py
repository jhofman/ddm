#!/usr/bin/env python
#
# file: simpleyql.py
#
# description: simple python function to interaction with YQL
#
# usage: ./simpleyql.py query env
#   where query is a valid YQL query
#   (see http://developer.yahoo.com/yql/console for examples)
#   and env is a YQL table enviroment
#   (e.g., store://datatables.org/alltableswithkeys)
#
# requirements:
#   simplejson (http://pypi.python.org/pypi/simplejson/)
#
# author: jake hofman (gmail: jhofman)
#

from urllib import urlencode
from urllib2 import urlopen
import simplejson as json
import sys

YQL_PUBLIC = 'http://query.yahooapis.com/v1/public/yql'

def yql_public(query, env=False):
    # build dictionary of GET parameters
    params = {'q': query, 'format': 'json'}
    if env:
        params['env'] = env
        
    # escape query
    query_str = urlencode(params)

    # fetch results
    url = '%s?%s' % (YQL_PUBLIC, query_str)
    result = urlopen(url)

    # parse json and return
    return json.load(result)['query']['results']

if __name__=='__main__':

    if len(sys.argv) >= 2:
        # take yql query from first command line argument
        query = sys.argv[1]
        if len(sys.argv) == 3:
            env = sys.argv[2]
        else:
            env = False
    else:
        # default to coffee near morningside heights
        query = 'select * from local.search where query="coffee" and location=10027'
        env = False
        
    print query

    # make call to yql
    results = yql_public(query, env)

    # pretty-print results
    print json.dumps(results, indent=2)

