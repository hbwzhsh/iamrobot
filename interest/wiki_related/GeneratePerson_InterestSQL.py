# coding=utf-8
__author__ = 'zhuwei'

import os
import sys
import simplejson
import time
import jsbeautifier
import thread
import multiprocessing
import curses

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
        outPutFile.write(data + "\n")


def GenerateSQL(data, TermWithIdANDName_List,x):
    CountLine = 1
    Person_Interest_Dict = {}
    Person_Interest_List = []
    startTime = time.clock()
    print startTime
    for eachLine in data:
        sys.stdout.write ("\r%s %s %.3f%% \n" % (x,('%%-%ds' % 100) % (100*CountLine/len(data) * '='), 100.0 * CountLine / len(data)))
        sys.stdout.flush()
        tmp_dict = {}
        tmp_list = eachLine.split("::")
        tmp_dict["id"] = tmp_list[0]
        tmp_dict["interests"] = tmp_list[1].replace("|||||\n", "").split("|||||")
        tmp_l = []
        tmp_ids = []
        for eachInterest in tmp_dict["interests"]:
            for eachTerm in TermWithIdANDName_List:
                tmpInterestWith = {}
                tmpInterestWith["term_name"] = eachInterest
                tmpInterestWith["term_id"]   = ""
                tmpInterestWith["related_term"] = ""
                if eachTerm["term_name"].encode('utf-8') == eachInterest:
                    tmpInterestWith["term_name"] = eachInterest
                    tmpInterestWith["term_id"] = eachTerm["id"]
                    tmpInterestWith["related_term"] = eachTerm["term_similars"]
                if tmpInterestWith['term_id'] in tmp_ids:
                    pass
                else:
                    tmp_ids.append(tmpInterestWith['term_id'])
                    tmp_l.append(tmpInterestWith)
        Person_Interest_Dict[tmp_list[0]] = tmp_l
        Person_Interest_List.append(tmp_dict)
        CountLine += 1
    init_SQL = 'INSERT INTO `51prof_main`.`prof_interests` (`id`,`person_id`,`interests`) VALUES (%s, %s, \'%s\')'
    for k, v in Person_Interest_Dict.iteritems():
        vs = simplejson.dumps(v).decode('unicode-escape').encode('utf-8')
        if vs <> '[]':
             sql = init_SQL % ("NULL", k, vs)
             Saving(sql)

def GeneratePerson_InterestSQL():
    global StartTime
    print StartTime
    Person_Interest_FileName = sys.argv[1]
    TermWithIdANDName_FileName = sys.argv[2]

    # Process TermWithRelatedTerm
    TermWithIdANDName_String = ReadFile(TermWithIdANDName_FileName)
    TermWithIdANDName_List = simplejson.loads(TermWithIdANDName_String)
    Person_Interest_Open = file(Person_Interest_FileName, 'r')
    Person_Interest_List1 = []
    Person_Interest_List2 = []
    Person_Interest_List3 = []
    Person_Interest_List4 = []
    Person_Interest_List5 = []
    Person_Interest_List6 = []
    Person_Interest_List7 = []
    Person_Interest_List8 = []
    Person_Interest_List9 = []
    Person_Interest_List10 = []
    Person_Interest_List11 = []
    LineCount = 1
    for eachLine in Person_Interest_Open:
        LineCount +=1
        if LineCount < 10000:
            Person_Interest_List1.append(eachLine)
        if LineCount >= 10000 and LineCount < 20000:
            Person_Interest_List2.append(eachLine)
        if LineCount >= 20000 and LineCount < 30000:
            Person_Interest_List3.append(eachLine)
        if LineCount >= 30000 and LineCount < 40000:
            Person_Interest_List4.append(eachLine)
        if LineCount >= 40000 and LineCount < 50000:
            Person_Interest_List5.append(eachLine)
        if LineCount >= 50000 and LineCount < 60000:
            Person_Interest_List6.append(eachLine)
        if LineCount >= 60000 and LineCount < 70000:
            Person_Interest_List7.append(eachLine)
        if LineCount >= 70000 and LineCount < 80000:
            Person_Interest_List8.append(eachLine)
        if LineCount >= 80000 and LineCount < 90000:
            Person_Interest_List9.append(eachLine)
        if LineCount >= 90000 and LineCount < 100000:
            Person_Interest_List10.append(eachLine)
        if LineCount >= 100000:
            Person_Interest_List11.append(eachLine)
    t1 = multiprocessing.Process(target=GenerateSQL,args=(Person_Interest_List1,TermWithIdANDName_List,1))
    t1.start()
    t2 = multiprocessing.Process(target=GenerateSQL, args=(Person_Interest_List2,TermWithIdANDName_List,2))
    t2.start()
    t3 = multiprocessing.Process(target=GenerateSQL, args=(Person_Interest_List3, TermWithIdANDName_List,3))
    t3.start()
    t4 = multiprocessing.Process(target=GenerateSQL, args=(Person_Interest_List4, TermWithIdANDName_List,4))
    t4.start()
    t5 = multiprocessing.Process(target=GenerateSQL, args=(Person_Interest_List5, TermWithIdANDName_List,5))
    t5.start()
    t6 = multiprocessing.Process(target=GenerateSQL, args=(Person_Interest_List6, TermWithIdANDName_List,6))
    t6.start()
    t7 = multiprocessing.Process(target=GenerateSQL, args=(Person_Interest_List7, TermWithIdANDName_List,7))
    t7.start()
    t8 = multiprocessing.Process(target=GenerateSQL, args=(Person_Interest_List8, TermWithIdANDName_List,8))
    t8.start()
    t9 = multiprocessing.Process(target=GenerateSQL, args=(Person_Interest_List9, TermWithIdANDName_List,9))
    t9.start()
    t10 = multiprocessing.Process(target=GenerateSQL, args=(Person_Interest_List10, TermWithIdANDName_List,10))
    t10.start()
    t11 = multiprocessing.Process(target=GenerateSQL, args=(Person_Interest_List11, TermWithIdANDName_List,11))
    t11.start()

if __name__ == "__main__":
    st = time.clock()
    GeneratePerson_InterestSQL()
    print "Finish, used %s" % (time.clock()-st)
