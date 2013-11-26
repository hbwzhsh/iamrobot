#coding=utf-8
__author__ = 'zhuwei'

import sys
import os
def Saving(data):
    with open("Person_Interest_utf8.sql", 'a+') as outPutFile:
        outPutFile.write(data + ";\n")

if __name__ == "__main__":
    fName = sys.argv[1]
    ff = file(fName, 'r')
    CountLine = 1
    for line in ff:
        CountLine +=1
        os.write(1,"\r %s Lines have finished! %.2f %%" % (CountLine,100.0*CountLine/112861))
        sys.stdout.flush()
        tmp_line = line
        tmp_line = tmp_line.replace("`51prof_main","`51prof_main`").replace('prof_interest','prof_interests')
        tmp_line = tmp_line.replace('"{',"'{").replace('}"',"}'")
        tmp_line = tmp_line.encode('utf-8').decode('unicode-escape').encode('utf-8')
        Saving(tmp_line)