import os
import sys
import re
import MySQLdb
import xml.etree.ElementTree as ET
from xml.sax import handler, parseString

reload(sys)
sys.setdefaultencoding("utf-8")

def insertMySQL(wiki_):
    try:
        conn=MySQLdb.connect(host='localhost', user='root',passwd='root123456',port=3306,charset='utf8')
        cur=conn.cursor()
        conn.select_db('pythontest')
        cur.execute('insert into wiki_zh values(NULL,%s,%s,%s)',wiki_)
        conn.commit()
        cur.close()
        conn.close()
        print "Insert Success"
        for i in range(len(wiki_)):
            print wiki_[i]
    except MySQLdb.Error, ee:
        print "MySQL error %d: %s" % (ee.args[0],ee.args[1])
in_sql = "insert into wiki_en(title,source,abstract) values(%s,%s,%s)"
fields = ("title","url","abstract")
class Db_Connect:  
    def __init__(self, db_host, user, pwd, db_name, charset="utf8",  use_unicode = True):  
        print "init begin"  
        print db_host, user, pwd, db_name, charset , use_unicode  
        self.conn = MySQLdb.Connection(db_host, user, pwd, db_name, charset=charset , use_unicode=use_unicode)  
        print "init end"  
    
    def insert(self, sql):
        try:
            n = self.conn.cursor().execute(sql)
            return n
        except MySQLdb.Warning, e:
            print "Error: execute sql '",sql,"' failed"
  
    def close(self):  
        self.conn.close()

class WikiHandler(handler.ContentHandler):  
    def __init__(self, db_ops):  
        #db op obj  
        self.db_ops = db_ops 
        self.doc = {}  
        self.current_tag = ""  
        self.in_quote = 0  
    def startElement(self, name, attr):  
        if name == "doc":  
            self.doc = {}  
        self.current_tag = name  
        self.in_quote = 1  
    def endElement(self, name):  
        if name == "doc":
            in_fields = tuple([('"'+re.sub('"',' ',self.doc.get(i,""))+' "')  for i in fields ])  
            print in_sql % in_fields  
            db_ops.insert( in_sql%(in_fields))  
        self.in_quote = 0  
    def characters(self, content):  
        if self.in_quote:  
            self.doc.update({self.current_tag: content})
if __name__ == "__main__":
    f = open(sys.argv[1])
    db_ops = Db_Connect("localhost","root","root123456","pythontest")
    parseString(f.read(), WikiHandler(db_ops))
    f.close()
    db_ops.close()
