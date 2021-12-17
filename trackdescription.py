import time
import os
import sys
import signal
import requests
import urllib

wikiSite = "en.wikipedia.org"
response = None

try:

    totalArticles = 0
    totalReverted = 0

    inFile = open("edits.txt", "r", encoding="utf-8")
    inLines = inFile.readlines()

    for inLine in inLines:
        inArr = inLine.split("\t")
        title = inArr[0]
        revId = inArr[2]
        print("Getting: " + title + ": " + revId)

        req = 'https://' + wikiSite + '/w/api.php?format=json&formatversion=2&action=query&redirects=1&prop=revisions&rvslots=main&rvprop=ids|timestamp|flags|comment|user|tags|content&rvlimit=50&rvdir=newer'
        req += '&titles=' + urllib.parse.quote(title)
        req += '&rvstartid=' + revId
        
        try:
            response = requests.get(req)
        except Exception as ex:
            print("Error during request.")
            print(repr(ex))

        json = response.json()

        first = True
        reverted = False
        initialDesc = ""
        finalDesc = ""

        if "revisions" not in json["query"]["pages"][0]:
            print("Warning: page does not exist.")
            continue

        for revision in json["query"]["pages"][0]["revisions"]:
            content = revision["slots"]["main"]["content"]
            t1 = content.lower().find("{{short description|")
            if t1 == -1:
                if not first: finalDesc = ""
                continue
            t1 += 20
            t2 = content.find("}}", t1 - 1)
            if t2 < t1:
                if not first: finalDesc = ""
                continue
            desc = content[t1:t2]
            desc = desc.replace("\n", "").replace("\t", "")
            if desc.lower() == "none":
                desc = ""
            
            if (first):
                first = False
                initialDesc = desc
                reverted = "mw-reverted" in revision["tags"] or "mw-manual-revert" in revision["tags"]
                if (reverted): break
            
            finalDesc = desc
        
        with open("out.txt", "a", encoding="utf-8") as outFile:
            outFile.write(inLine.replace("\n", "") + "\t" + initialDesc + "\t" + finalDesc + "\n")
        

        totalArticles += 1
        if reverted or len(finalDesc) == 0:
            totalReverted += 1
        print(">> Revert rate: " + str(float(totalReverted * 100) / totalArticles))


        if reverted:
            print("    > reverted!")
            continue

        print("    start-> " + initialDesc)
        print("    end---> " + finalDesc)

        time.sleep(1)


except KeyboardInterrupt:
    sys.exit(0)
except Exception as e:
    print(repr(e))
    print(response.text)
