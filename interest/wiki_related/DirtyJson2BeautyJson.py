#coding=utf-8
__author__ = 'zhuwei'
import jsbeautifier
import simplejson
import sys
import os

def read_with_progress(old_json_F):
    totalSize = os.path.getsize(sys.argv[1])
    totalRead = 0
    while True:
        old_json_F_read =  old_json_F.read(1024)
        if not old_json_F_read:
            old_json_F.close()
            break;
        totalRead += len(old_json_F_read)
        os.write(1, "Progress : %s persent" % (totalRead/totalSize))
        sys.stdout.flush()
        yield old_json_F_read
    #return old_json_F_read
if __name__ == "__main__":
    old_json_F = open(sys.argv[1], 'r')
    #for old_json_F_read in read_with_progress(old_json_F):
    #old_json_F_read = read_with_progress(old_json_F)
    old_json_F_read = old_json_F.read()
    # old_json_F_read.replace("\n","")
    # old_json_F_read.replace("\r","")
    old_json_F_read = jsbeautifier.beautify(old_json_F_read)
    old_json_list = simplejson.loads(old_json_F_read.replace("||||\n",'||||'))

    print "success"