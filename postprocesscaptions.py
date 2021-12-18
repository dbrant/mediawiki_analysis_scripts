import time
import os
import sys
import signal
import requests
import urllib

# take each line in the input file, parse out the image caption that was
# added, and append it to the same line in a new file.

inFileName = sys.argv[1]
outFileName = sys.argv[2]

inFile = open(inFileName, "r", encoding="utf-8")
inLines = inFile.readlines()

outFile = open(outFileName, "w", encoding="utf-8")

for inLine in inLines:
    comment = inLine.split("\t")[5]
    t1 = comment.find(" */") + 4
    t2 = comment.find(", #suggest", t1)
    caption = comment[t1:t2]
    outFile.write(inLine.replace("\n", "") + "\t" + caption + "\n")
