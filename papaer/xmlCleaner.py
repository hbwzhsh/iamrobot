# coding=utf-8

import sys
import os
import re

__author__ = 'zhuwei'

def ReadFile(filename):
    global bufferSize
    bufferSize = 50000
    File = file(filename, 'r')
    buffer = File.read(bufferSize)
    TotalSize = os.path.getsize(filename)
    fileS = ""
    while len(buffer):
        fileS += buffer
        fProgress = 100.0 * len(fileS) / TotalSize
        os.write(1, "\r Progress[%.3f %% (%d/%d)]" % (fProgress, len(fileS), TotalSize))
        sys.stdout.flush()
        buffer = File.read(bufferSize)
    File.close()
    print "\n Read File %s Finished" % filename
    return fileS
def Saving(data):
    with open("/sdd/zhuwei/prof_data/paperWithPerson.lcj", 'a+') as outPutFile:
        outPutFile.write(data)
if __name__ =="__main__":
    f = file(sys.argv[1],'r')
    Count = 1
    pat = re.compile(r'<(?!(title|paper|/|authors|time|papers|source|id|personid))')
    pat2 = re.compile(r'(?<!title)(?<!paper)(?<!/)(?<!authors)(?<!time)(?<!papers)(?<!id)(?<!personid)(?<!source)>')
    pat3 = re.compile(r'&(?!(lt;|gt;|nbsp;))')
    for line in f.readlines():
        sys.stdout.write("\r%.3f %% finished %s" % (100.0*Count/11842920,('%%-%ds' % 100) % (100*Count/11842920 * '=')))
        sys.stdout.flush()
        Count += 1
        tmp = line.replace('\\ <','&lt;').replace("& nbsp ; ","").replace("& nbsp ;","").replace("& nbsp","").replace("nbsp","")
        tmp = re.sub(pat3,'&amp;',tmp)
        tmp = re.sub(pat,'&lt;',tmp)
        tmp = re.sub(pat2,'$gt;',tmp)
        tmp = tmp.replace("&lt; br $gt;","")
        Saving(tmp)