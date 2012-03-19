#!/bin/bash

# grab source for team page
# break on equal signs before hrefs
# match on urls for 3-letter team codes
# print full urls
# download each team page with wget

curl 'http://sports.yahoo.com/nhl/teams' | \
   tr = '\n' | \
   grep '/nhl/teams/[a-z]*' | \
   awk -F'"' '{print "http://sports.yahoo.com"$2}' | \
   xargs wget	     				      	

