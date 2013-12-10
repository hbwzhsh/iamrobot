# coding=utf-8
import sys
import os
import re
from xml.sax import handler, parseString

reload(sys)
sys.setdefaultencoding('utf-8')

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

class Generate_SQL:
    def __init__(self, initSQL):
        self.initSQL = initSQL

    def save(self, data):
        with open("/sdc/zhuwei/prof_data/paper.sql", 'a+') as paperFile:
            paperFile.write(data+"\n")

    def generate(self, data):
        self.SQL = self.initSQL % data
        return self.SQL


class PaperHandler(handler.ContentHandler):
    def __init__(self, genSQL):
        self.doc = {}
        self.genSQL = genSQL
        self.current_tag = ""
        self.in_quote = 0
        self.count = 1

    def startElement(self, name, attr):
        if name == "paper":
            self.doc = {}
        self.current_tag = name
        self.in_quote = 1

    def endElement(self, name):
        if name == "paper":
            if self.doc.get('title','') <> "":
                in_fields = tuple([('"'+re.sub(u"(?<=[\u4e00-\u9fa5]) (?=[\u4e00-\u9fa5])",'',self.doc.get(i, "").replace(' - ','-').replace('"','\\\"'))+'"') for i in fields ])
                SQL = genSQL.generate(in_fields).encode('utf-8')
                #SQL = re.sub(r'(?!title|paper|/|authors|time|papers|source|id|personid)>','&gt;',SQL)
                genSQL.save(SQL)
                self.count +=1
                sys.stdout.write("\r%.3f%% Finished %s" % (100.0*self.count/1480365,('%%-%ds' % 100) % (100*self.count/1480365 * '=')))
                sys.stdout.flush()
        self.in_quote = 0

    def characters(self, content):
        if self.in_quote:
            self.doc.update({self.current_tag: content})

if __name__ == "__main__":
    #f = open(sys.argv[1])
    initSQL = "insert into `51prof_main`.`person_papers` (`id`, `title`, `source`, `time`, `authors`, `personid`) VALUES(NULL, %s, %s, %s, %s, %s);"
    fields = ("title", "source", "time", "authors", "personid")
    genSQL = Generate_SQL(initSQL)
    parseString(ReadFile(sys.argv[1]), PaperHandler(genSQL))