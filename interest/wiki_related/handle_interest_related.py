# coding=utf-8
# 本脚本用于处理相似兴趣，处理好插入数据库
# @author zhuwei@ict.ac.cn
# @since v0.1
# @uses OS SYS RE MYSQLDB
# @date 2013-11-16
import os
import sys
import re
import MySQLdb
import getpass

reload(sys)
sys.setdefaultencoding("utf-8")

def testMysql(wiki_):
    try:
        conn=MySQLdb.connect(host='172.16.48.205',user='root',passwd='227742364',port=3306,charset='utf8')
        cur=conn.cursor()
        conn.select_db('51prof_main')
        testResult = cur.execute('SELECT * from wiki_zh where title="%s"' % wiki_)
        if testResult == 0:
            print "No result"
        else:
            print "fail test"
    except MySQLdb.Error, ee:
        print "MySQL error %d : %s" % (ee.args[0], ee.args[1])

def inserttoMysql(interest):
    try:
        conn=MySQLdb.connect(host='172.16.48.205', user='root',passwd='227742364',port=3306,charset='utf8')
        cur=conn.cursor()
        conn.select_db('51prof_main')
        # print 'UPDATE wiki_zh SET related_wiki= %s WHERE title=%s' % (interest[1], interest[0])
        select_result = cur.execute('SELECT * from wiki_zh where title="%s"' % interest[0])
        if select_result == 0:
            return
        else:
            sql = 'UPDATE wiki_zh SET related_wiki="%s" WHERE title="%s";' % (interest[1],interest[0])
            count += 1
            if(count > 1000):
                cur.execute('UPDATE wiki_zh SET related_wiki= "%s" WHERE title="%s"' % (interest[1], interest[0]))
                conn.commit()
            print "Insert Success"
        cur.close()
        conn.close()
    except MySQLdb.Error, ee:
        print "MySQL error %d: %s" % (ee.args[0],ee.args[1])
if __name__ == "__main__":
    f = open(sys.argv[1])
    host = sys.argv[2]
    user = sys.argv[3]
    passwd = getpass.getpass('password:')
    sql = ""
    try:
        conn = MySQLdb.connect(host, user ,passwd , port=3306, charset='utf8')
        cur=conn.cursor()
        conn.select_db('51prof_main')
        for line in f:
            tmp = line.split(":")
            if len(tmp) > 1:
                tmp[1] = tmp[1].strip('\n').strip()
                sql +='UPDATE wiki_zh SET `related_wiki`="%s" where title="%s";' % (tmp[1],tmp[0])
                # print sql
            else:
                print "Null"
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        print "Insert Success!"
    except MySQLdb.Error, ee:
        print "MySQL error %d: %s" % (ee.args[0], ee.args[1])
    print "Finished!"
