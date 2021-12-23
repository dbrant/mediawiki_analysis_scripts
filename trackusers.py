import time
import os
import sys
import signal
import requests
import urllib

inFileName = sys.argv[1]
outFileName = sys.argv[2]
wikiSite = "en.wikipedia.org"
response = None

try:

    inFile = open(inFileName, "r", encoding="utf-8")
    inLines = inFile.readlines()

    users = []

    for inLine in inLines:
        inArr = inLine.split("\t")
        title = inArr[0]
        revId = inArr[2]
        userName = inArr[3]
        users.append(userName)
    
    users = set(users)

    outFile = open(outFileName, "w", encoding="utf-8")

    for user in users:

        print("> " + user)
        line = user + "\t"
        editCodes = []

        continueStr = ""
        while True:

            req = 'https://' + wikiSite + '/w/api.php?format=json&formatversion=2&action=query&list=usercontribs&&uclimit=100&ucnamespace=0&ucprop=ids|title|timestamp|comment|size|flags|tags'
            req += '&ucuser=' + urllib.parse.quote(user)
            if len(continueStr) > 0:
                req += "&uccontinue=" + continueStr
            
            try:
                response = requests.get(req)
            except Exception as ex:
                print("Error during request.")
                print(repr(ex))
            
            json = response.json()

            continueStr = json["continue"]["uccontinue"] if "continue" in json else ""

            for contrib in json["query"]["usercontribs"]:
                comment = contrib["comment"] if "comment" in contrib else ""
                isSuggestedEdit = "#suggested" in comment
                isReverted = "mw-reverted" in contrib["tags"]

                if isSuggestedEdit:
                    if isReverted:
                        editCodes.append("3")
                    else:
                        editCodes.append("2")
                else:
                    if isReverted:
                        editCodes.append("1")
                    else:
                        editCodes.append("0")

            if len(continueStr) == 0 or len(editCodes) > 5000: break
        
        editCodes.reverse()

        line += ",".join(editCodes)
        line += "\n"
        outFile.write(line)


except KeyboardInterrupt:
    sys.exit(0)
except Exception as e:
    print(repr(e))
    print(response.text)
