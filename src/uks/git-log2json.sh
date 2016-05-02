#!/usr/bin/env bash
git log --date=format:'%Y-%m-%d %H:%M:%S' --pretty=format:'{  "commit": "%H",  "author": "%an <%ae>",  "date": "%ad",  "message": "%f"}' $@ | perl -pe 'BEGIN{print ""}; END{print "\n"}' | perl -pe 's/},]/}]/'> log.json

