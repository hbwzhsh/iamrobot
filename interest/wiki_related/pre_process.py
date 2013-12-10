# coding=utf-8
# encoding: utf-8
'''
@filename        : pre_process.py
@authors         : <mailto:zhuwei.ict.ac.cn>
@date            : 2013-11-19
@version         : 1.0
@company         : ICT
'''
# 处理研究兴趣

__author__ = 'zhuwei'
import re
import sys
import os
import time
import jsbeautifier
import simplejson

g_nTotal = 100
g_nProccessed = 0
g_fStartTime = time.time()

# json 数据格式化
def process(data, outFile):
    global g_nProccessed
    data = jsbeautifier.beautify(data)
    #data = data.replace('|||||\n"\n}', '|||||"\n}')
    with open(outFile, 'w+') as outputFile:
        outputFile.write(data)

#　文件读取、预处理函数
def pre_proccess(g_fread, outFile=1, ifBeauty=0):
    global g_nProccessed
    global g_fStartTime
    global g_nTotalSize
    bufferSize = 50000
    g_fStartTime = time.time()
    buffer = g_fread.read(bufferSize)
    fileS = ""
    while len(buffer):
        fileS += buffer
        fPrograss = 100.0 * len(fileS) / g_nTotalSize
        os.write(1, "\rProgress[%.3f %% (%d/%d)]" % (fPrograss, len(fileS), g_nTotalSize))
        sys.stdout.flush()
        buffer = g_fread.read(bufferSize)
    if ifBeauty == 1:
        process(fileS, outFile)
    else:
        print "\n"
        return fileS

# 结果存储函数
def SaveResults(data, FileName, IsJson=1):
    if IsJson == 1:
        data = jsbeautifier.beautify(data)
    with open(FileName, 'a+') as outputFile:
        outputFile.write(data)


def GenerateSQL(data):
    tmpsql = "UPDATE `prof_tags` set `interests`=\"%s\" WHERE `person_id`=%s \n" % (
        data["interests"].encode('utf-8').replace("||||||||||", "").replace("\n", ""), data["id"])
    return tmpsql


def GenerateJSON(data):
    tmpjson = simplejson.dumps(data).decode('unicode_escape').encode('utf-8').replace("||||||||||", "").replace("\n",
                                                                                                                "")
    return tmpjson


if __name__ == "__main__":
    global StartTime
    global EndTime
    global g_nTotalSize

    StartTime = time.clock()

    if sys.argv[3] == "-o":
        g_nTotalSize = os.path.getsize(sys.argv[1])
        BeautyJsonF = file(sys.argv[1])
        BeautyJsonRead = pre_proccess(BeautyJsonF)
        Json2List = simplejson.loads(BeautyJsonRead)
        BeautyJsonF.close()

        g_nTotalSize = os.path.getsize(sys.argv[2])
        lcjRelatedInterestFile = file(sys.argv[2])
        lcjRelatedInterestDict = {}
        CountLine = 0

        for eachLine in lcjRelatedInterestFile:
            os.write(1, "\r %d Lines have been read, %.3f %% Finished, %s Seconds have been spent" % (
                CountLine, 100.0 * CountLine / 449082, time.clock() - StartTime))
            tmp_list = eachLine.split("[[:]]")
            key = tmp_list[0].decode('utf-8')
            value = tmp_list[1].decode('utf-8')
            lcjRelatedInterestDict[key] = value
            CountLine += 1
            sys.stdout.flush()
        lcjRelatedInterestFile.close()
        count = 0
        for element in Json2List:
            tmp_elememt = element["interests"]
            tmp_elememt = tmp_elememt.split('|||||')
            tmp_str = ""
            for i in range(len(tmp_elememt)):
                if (tmp_elememt[i] <> "" and lcjRelatedInterestDict.has_key(tmp_elememt[i])):
                    tmp_elememt[i] += "[[:]]" + lcjRelatedInterestDict[tmp_elememt[i]]
                    count += 1
                tmp_str += tmp_elememt[i] + "|||||"
            element["interests"] = tmp_str
        OutPutFileName = raw_input("\nInput the output filename: ")
        ResultJson = "["
        TotalLen = float(len(Json2List))

        for j in range(len(Json2List)):
            os.write(1, "\r %d Lines have been processed, %.3f %%, %s Seconds have been spent" % (
                j, 100.0 * j / TotalLen, time.clock() - StartTime))
            tmpsql = GenerateSQL(Json2List[j])
            SaveResults(tmpsql, OutPutFileName, IsJson=0)
            sys.stdout.flush()
        EndTime = time.clock()
        print count
        print "Finish! Total costs " + bytes(EndTime - StartTime) + " seconds"
        #print len(Json2List)
    else:
        g_nTotalSize = os.path.getsize(sys.argv[1])
        print "Total File Size is %s" % g_nTotalSize
        f = file(sys.argv[1], 'r')
        pre_proccess(f, sys.argv[2], 1)
        f.close()