#coding:utf-8
import os
import sys
import MySQLdb

try:
    conn=MySQLdb.connect(host='172.16.1.43',user='root',passwd='root123456',port=3306)
    cur=conn.cursor()
    conn.select_db('pythontest')
    cur.execute('create table exp_time(id int, timenode varchar(20), start_time varchar(20),end_time varchar(20), department varchar(20),institute varchar(20),event varchar(50),title varchar(20))')
    conn.commit()
    cur.close()
    conn.close()
except MySQLdb.Error, e:
    print "Mysql Error %d: %s" % ( e.args[0], e.args[1] )

def insertMySQL(exp):
    for i in range(len(exp)):
        if type(exp[i]).__name__ == "unicode":
            exp[i] = exp[i].decode('utf8')
    try:
        conn=MySQLdb.connect(host='172.16.1.43', user='root', passwd='root123456', port=3306, charset='utf8')
        cur=conn.cursor()
        conn.select_db('pythontest')
        cur.execute('insert into exp_time values(%s,%s,%s,%s,%s,%s,%s,%s)', exp )
        cur.execute('update test set info="I am python" where id=3')
        conn.commit()
        cur.close()
        conn.close()
        print "Insert Success"
        for i in range(len(exp)):
            print exp[i]
    except MySQLdb.Error, e:
        print "MySQL error %d: %s" % (e.args[0], e.args[1])

dirlist = os.listdir('/sdd/gc14_home_bak/sjc/NER_RE/TOOLS/crf/zhuresults')
for listname in dirlist:
    dirname = os.path.join('/sdd/gc14_home_bak/sjc/NER_RE/TOOLS/crf/zhuresults',listname)
    file = open(dirname)
    exp = [listname,"","","","","","",""]
    for line in file:
        if cmp(line, '\n') != 0:
            if line.endswith(' tim-B\n'):
                exp[1] = line.rstrip('tim-B\n')
            elif line.endswith('stim-B\n'):
                exp[2] = line.rstrip('stim-B\n')
            elif line.endswith('etim-B\n'):
                exp[3] = line.rstrip('etim-B\n')
            elif line.endswith('depa-B\n'):
                exp[4] = line.rstrip('depa-B\n')
            elif line.endswith('comp-B\n'):
                exp[5] = line.rstrip('comp-B\n')
            elif line.endswith('eve-B\n'):
                exp[6] = line.rstrip('eve-B\n')
            elif line.endswith('titl-B\n'):
                exp[7] = line.rstrip('titl-B\n')
        else:
            insertMySQL(exp)
            exp = [listname, "","","","","","",""]

