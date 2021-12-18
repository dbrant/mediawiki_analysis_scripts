import time
import os
import sys
import signal
import requests
import urllib

# parse out edits only from the Wikipedia app (since some edits came from
# the Commons app, and are also tagged with "android-app-edit").

inFile = open("enwiki_android_app_edit.txt", "r", encoding="utf-8")
inLines = inFile.readlines()

outFile = open("enwiki_android_app_edit__.txt", "w", encoding="utf-8")

for inLine in inLines:
    
    if ("#suggested" in inLine) or ("add-depicts:" in inLine):
        outFile.write(inLine)
