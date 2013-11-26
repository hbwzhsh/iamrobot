# coding=utf-8
__author__ = 'zhuwei'

import os
import sys
import simplejson
import time
import jsbeautifier


# Globals
global StartTime
global bufferSize

bufferSize = 50000
StartTime = time.clock()


def ReadFile(filename):
    global bufferSize
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


def GenerateJSON(data):
    pass


def GenerateSQL(data):
    pass


def Saving(data):
    with open("Person_Interest.sql", 'a+') as outPutFile:
        outPutFile.write(data + ";\n")


def GeneratePerson_InterestSQL():
    global StartTime
    Person_Interest_FileName = sys.argv[1]
    TermWithIdANDName_FileName = sys.argv[2]

    # Process TermWithRelatedTerm
    TermWithIdANDName_String = ReadFile(TermWithIdANDName_FileName)
    TermWithIdANDName_List = simplejson.loads(TermWithIdANDName_String)

    StartTime = time.clock()
    CountLine = 1
    StartTime = time.clock()
    Person_Interest_Open = file(Person_Interest_FileName,'r')
    Person_Interest_List = []
    Person_Interest_Dict = {}

    for eachLine in Person_Interest_Open:
        os.write(1, "\r %d Lines have read, %.3f %% Finished, %s Seconds have cost" % (
        CountLine, 100.0 * CountLine / 112861, time.clock() - StartTime))
        tmp_dict = {}
        tmp_list = eachLine.split("::")
        tmp_dict["id"] = tmp_list[0]
        tmp_dict["interests"] = tmp_list[1].replace("|||||\n","").split("|||||")
        #Person_Interest_Dict[tmp_list[0]] = tmp_dict["interests"]
        for eachInterest in tmp_dict["interests"]:
            for eachTerm in TermWithIdANDName_List:
                if eachTerm["term_name"].encode('utf-8') == eachInterest:
                    tmpInterestWith = {}
                    tmpInterestWith["term_name"] = eachInterest
                    tmpInterestWith["term_id"] = eachTerm["id"]
                    tmpInterestWith["related_term"] = eachTerm["term_similars"]
                    Person_Interest_Dict[tmp_list[0]] = tmpInterestWith
        Person_Interest_List.append(tmp_dict)
        CountLine += 1
        sys.stdout.flush()
    Person_Interest_Open.close()
    init_SQL = 'UPDATE `51prof_main`.`prof_interests` SET  `interests`=\'%s\' WHERE `prof_interests` . `person_id` = %s'
    for k,v in Person_Interest_Dict.iteritems():
        v = simplejson.dumps(v)
        sql = init_SQL % (v,k)
        Saving(sql)
if __name__ == "__main__":
    GeneratePerson_InterestSQL()