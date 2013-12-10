#coding=utf-8
__author__ = 'zhuwei'

import sys
import os
def Saving(data):
    with open("Person_Interest_semicolon.sql", 'a+') as outPutFile:
        outPutFile.write(data)
if __name__ == "__main__":
    fName = sys.argv[1]
    CountLine = 1
    for line in file(fName,'r'):
        CountLine += 1
        os.write(1,"\r %s Lines have finished! %.2f %%" % (CountLine,100.0*CountLine/112861))
        sys.stdout.flush()
        tmp_line = line.decode('utf-8').replace('\n','').replace('\'an',"^an").replace('\'s ','^s ')
        tmp_line += ";\n"
        Saving(tmp_line.encode('utf-8'))
