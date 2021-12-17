import time
import os
import sys
import signal
import requests

wikiSite = "en.wikipedia.org"
response = None

try:
    curContinue = ""
    while True:
        print("Fetching data with continuation: " + curContinue)

        req = 'https://' + wikiSite + '/w/api.php?format=json&formatversion=2&action=query&list=recentchanges&rcnamespace=0&rclimit=100&rctag=android app edit&rcprop=title|timestamp|ids|flags|comment|user|loginfo|tags'
        if len(curContinue) > 0:
            req += '&rccontinue=' + curContinue

        response = requests.get(req)
        json = response.json()

        curContinue = json["continue"]["rccontinue"]

        with open("out.txt", "a", encoding="utf-8") as outFile:
            for change in json["query"]["recentchanges"]:
                if "comment" not in change:
                    continue
                if "#suggested" not in change["comment"]:
                    continue
                outFile.write(change["title"] + "\t" + str(change["pageid"]) + "\t" + str(change["revid"]) + "\t" + change["user"] + "\t"
                + change["timestamp"] + "\t" + change["comment"] + "\t" + ','.join(change["tags"]) + "\n")

        time.sleep(5)

except KeyboardInterrupt:
    sys.exit(0)
except Exception as e:
    print(repr(e))
    print(response.text)
