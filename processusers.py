import time
import os
import sys
import signal
import requests
import urllib

inFileName = sys.argv[1]
outFileName = sys.argv[2]

try:

    inFile = open(inFileName, "r", encoding="utf-8")
    inLines = inFile.readlines()

    userDict = {}

    for inLine in inLines:
        inArr = (inLine.replace("\n", "")).split("\t")
        userName = inArr[0]
        editCodes = inArr[1].split(",")
        userDict[userName] = editCodes
    
    userDict = sorted(userDict.items(), key=lambda item: len(item[1]))

    outFile = open(outFileName, "w", encoding="utf-8")
    outFile.write('<html><head><meta charset="utf-8" /><link rel="stylesheet" href="main.css" /></head><body>\n')


    targetUsers = 0



    for item in userDict:
        userName = item[0]
        editCodes = item[1]



        isTargetUser = False
        first = True
        for code in editCodes:
            if (len(code) == 0): continue
            if first:
                first = False
                if int(code) != 2: break
            else:
                if int(code) == 0:
                    isTargetUser = True
                    break

        if len(editCodes) < 4:
            isTargetUser = False

        if isTargetUser:
            print(">>> " + userName)
            targetUsers += 1
        
        
        if not isTargetUser: continue



        outFile.write("<div>")
        outFile.write('<div class="username"><a href="https://en.wikipedia.org/wiki/Special:Contributions/' + userName + '">' + userName + "</a></div>")

        for code in editCodes:
            if len(code) == 0: continue

            if int(code) == 0:
                outFile.write('<span class="edit"></span>')
            elif int(code) == 1:
                outFile.write('<span class="edit_rev"></span>')
            elif int(code) == 2:
                outFile.write('<span class="se"></span>')
            elif int(code) == 3:
                outFile.write('<span class="se_rev"></span>')

        outFile.write("</div>\n")
    
    outFile.write("</body></html>")

    print(">>> Total target users: " + str(targetUsers))

except KeyboardInterrupt:
    sys.exit(0)
except Exception as e:
    print(repr(e))
    print(response.text)
