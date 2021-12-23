import time
import os
import sys
import signal
import requests
import urllib

inFileName = sys.argv[1]
totalEdits = 0
totalReverted = 0

inFile = open(inFileName, "r", encoding="utf-8")
inLines = inFile.readlines()

for inLine in inLines:
    inArr = inLine.split("\t")
    title = inArr[0]
    revId = inArr[2]
    userName = inArr[3]
    tags = inArr[6]
    #anon = inArr[7]

    anon = (userName.find(".") > 0) or (userName.find(":") > 0)

    if not anon: continue

    if "android app edit" not in tags: continue

    reverted = "mw-reverted" in tags

    print("> " + title)

    totalEdits += 1
    if reverted:
        totalReverted += 1
    print(">> Revert rate: " + str(float(totalReverted * 100) / totalEdits))

print("Total edits: " + str(totalEdits))
print("Total reverts: " + str(totalReverted))
