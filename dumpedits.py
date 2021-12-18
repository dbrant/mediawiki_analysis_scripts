import time
import os
import sys
import signal
import requests

#wikiSite = "www.wikidata.org"
wikiSite = "en.wikipedia.org"
tagFilter = "android app edit"
olderThanTime = "" #"2021-11-30T17:23:37.000Z"
response = None

try:
    curContinue = ""
    while True:

        req = 'https://' + wikiSite + '/w/api.php?format=json&formatversion=2&action=query&list=recentchanges&rcnamespace=0&rclimit=100&rcprop=title|timestamp|ids|flags|comment|user|loginfo|tags'
        req += '&rctag=' + tagFilter
        if len(olderThanTime) > 0:
            req += '&rcdir=older&rcstart=' + olderThanTime
        if len(curContinue) > 0:
            req += '&rccontinue=' + curContinue

        print("Making request: " + req)

        response = requests.get(req)
        json = response.json()

        curContinue = json["continue"]["rccontinue"]

        with open("edits.txt", "a", encoding="utf-8") as outFile:
            for change in json["query"]["recentchanges"]:
                if "comment" not in change:
                    continue
                #if "#suggested" not in change["comment"]:
                #    continue
                outFile.write(change["title"] + "\t" + str(change["pageid"]) + "\t" + str(change["revid"]) + "\t" + change["user"] + "\t"
                + change["timestamp"] + "\t" + change["comment"] + "\t" + ','.join(change["tags"]) + "\n")

        time.sleep(5)

except KeyboardInterrupt:
    sys.exit(0)
except Exception as e:
    print(repr(e))
    print(response.text)
