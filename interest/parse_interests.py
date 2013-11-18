# import os
import sys
# import re
import MySQLdb

reload(sys)
sys.setdefaultencoding("utf-8")


def inserttoMysql(interest):
    try:
        conn = MySQLdb.connect(host='172.16.48.205', user='root', passwd='227742364', port=3306, charset='utf8')
        cur = conn.cursor()
        conn.select_db('rsearch_gd13_125')
        print 'UPDATE researchers SET interest_tag= %s WHERE id = %s' % (interest[1], interest[0])
        cur.execute('UPDATE researchers SET interest_tag= "%s" WHERE id=%s' % (interest[1], interest[0]))
        conn.commit()
        cur.close()
        conn.close()
        print "Insert Success"
    except MySQLdb.Error, ee:
        print "MySQL error %d: %s" % (ee.args[0], ee.args[1])


if __name__ == "__main__":
    f = open(sys.argv[1])
    for line in f:
        tmp = line.split("::")
        inserttoMysql(tmp)