# coding=utf-8
# encoding: utf-8
'''
@filename      : GenerateTermSQL.py
@authors       : <mailto:zhuwei@ict.ac.cn>
@date          : 2013-11-21
@version       : 1.0
@company       : ICT
'''
__author__ = 'zhuwei'

import sys
import time
import os
import jsbeautifier
import simplejson

reload(sys)
sys.setdefaultencoding("utf-8")
# Globals
global pyStartTime

pyStartTime = time.clock()


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
    with open("TermSQL.sql", 'a+') as outPutfile:
        outPutfile.write(data + ";\n")


if __name__ == "__main__":
    init_SQL = 'INSERT INTO `51prof_main`.`prof_terms`(`id`, `term_name`, `term_similars`,`term_wiki_id`) VALUES (%s, "%s", "%s", %s)'
    log = file("GenerateTermSQL.log", 'a+')
    countLine = 1
    termWithRelatedTerm_file = file(sys.argv[1], 'r')
    termWithRelatedTerm_Dict = {}
    pyStartTime = time.clock()
    for eachLine in termWithRelatedTerm_file:
        os.write(1, "\r %d Lines have read, %.3f %% finished, %s Seconds have cost" % (
            countLine, 100.0 * countLine / 64737, time.clock() - pyStartTime))
        tmpTermWithRelatedTerm_List = eachLine.split("[[:]]")
        key = tmpTermWithRelatedTerm_List[0]
        value = tmpTermWithRelatedTerm_List[1]
        termWithRelatedTerm_Dict[key] = value
        countLine += 1
    termWithRelatedTerm_file.close()
    termWithOutRelatedTerm_List = termWithRelatedTerm_Dict.keys()

    # Read wiki file
    wikiWithIdANDTitle = ReadFile(sys.argv[2])
    wikiWithIdANDTitle_LIST = simplejson.loads(wikiWithIdANDTitle)
    countKey = 1
    for i in wikiWithIdANDTitle_LIST:
        tmpWikiId = i["id"]
        tmpWikiTitle = str(i["title"]).encode('utf-8')
        try:
            if termWithOutRelatedTerm_List.index(tmpWikiTitle):
                os.write(1, "\rProgress %.3f %% Finished [%d/%d]" % (
                    100.0 * countKey / len(wikiWithIdANDTitle_LIST), countKey, len(wikiWithIdANDTitle_LIST)))
                sys.stdout.flush()
                sql = init_SQL % (
                "NULL", tmpWikiTitle, termWithRelatedTerm_Dict[tmpWikiTitle].replace("[[|]]\n", ""), tmpWikiId)
                del termWithRelatedTerm_Dict[tmpWikiTitle]
                countKey += 1
                Saving(sql)
        except ValueError, e:
            log.write(str(e) + "\n")
            countKey += 1
    countKey = 1
    for key in termWithRelatedTerm_Dict:
        os.write(1, "\rProgress %.3f %% Finished [%d/%d]" % (
            100.0 * countKey / len(termWithRelatedTerm_Dict), countKey, len(termWithRelatedTerm_Dict)))
        sys.stdout.flush()
        sql = init_SQL % ("NULL", key, termWithRelatedTerm_Dict[key], "NULL")
        Saving(sql)
        #pass