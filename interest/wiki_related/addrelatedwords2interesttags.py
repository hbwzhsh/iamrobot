# coding=utf-8
__author__ = 'zhuwei'

import simplejson
#import json
import jsbeautifier
import sys
import re

if __name__ == "__main__":
    # old_json = sys.argv[1]
    # to_be_add = sys.argv[2]
    # output = sys.argv[3]`
    old_json_F = open(sys.argv[1], 'r')
    old_json_F_read = old_json_F.read()
    old_json_F_read = jsbeautifier.beautify(old_json_F_read)
    old_json_list = simplejson.loads(old_json_F_read)
    print "Success"
#old_List = json.dump(old_json)
