import time
import os
import sys
import signal
import requests

outFileName = sys.argv[1]
#wikiSite = "www.wikidata.org"
wikiSite = "en.wikipedia.org"
tagFilter = "android app edit"
namespace = "0"
olderThanTime = "" #"2021-12-10T17:23:37.000Z"
response = None

try:
    outFile = open(outFileName, "a", encoding="utf-8")

    curContinue = ""
    while True:

        req = 'https://' + wikiSite + '/w/api.php?format=json&formatversion=2&action=query&list=recentchanges&rctype=edit&rclimit=100&rcprop=title|timestamp|ids|flags|comment|user|loginfo|tags'
        req += "&rcnamespace=" + namespace
        if len(tagFilter) > 0:
            req += '&rctag=' + tagFilter
        if len(olderThanTime) > 0:
            req += '&rcdir=older&rcstart=' + olderThanTime
        if len(curContinue) > 0:
            req += '&rccontinue=' + curContinue

        print("Making request: " + req)

        response = requests.get(req)
        json = response.json()

        curContinue = json["continue"]["rccontinue"]

        for change in json["query"]["recentchanges"]:
            if "comment" not in change:
                continue
            if "#suggested" not in change["comment"]:
                continue
            comment = change["comment"].replace("\n", " ").replace("\t", " ")
            outFile.write(change["title"] + "\t" + str(change["pageid"]) + "\t" + str(change["revid"]) + "\t" + (change["user"] if "user" in change else "") + "\t"
            + change["timestamp"] + "\t" + comment + "\t" + ','.join(change["tags"]) + "\t" + ("1" if "anon" in change else "0") + "\n")

        time.sleep(1)

except KeyboardInterrupt:
    sys.exit(0)
except Exception as e:
    print(repr(e))
    print(response.text)
