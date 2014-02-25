#coding=utf-8
__author__ = 'Tadimy'

import sys
import os
import datetime
import optparse
import jsbeautifier
import simplejson
import time
import re


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


def format_time(original_time=''):
    original_time = original_time.strip().encode('utf-8')
    original_time = original_time.replace('-', '')
    t = original_time
    pat_find_0 = re.findall(r'[0-9]', original_time)
    if len(pat_find_0) < 2:
        return '0000-00'
    elif original_time.find('年') != -1:
        if len(original_time) == 5:
            t = datetime.datetime.strptime(original_time, '%y年').strftime('%Y-%m')
        elif len(original_time) == 7:
            t = datetime.datetime.strptime(original_time, '%Y年').strftime('%Y-%m')
        elif len(original_time) == 9:
            pat_find_1 = re.findall(r'[0-9]+',original_time)
            if len(pat_find_1) == 2:
                if len(pat_find_1[0]+pat_find_1[1]) < 4:
                    t = datetime.datetime.strptime(pat_find_1[0] + pat_find_1[1],'%y%m').strftime('%Y-%m')
                else:
                    t = datetime.datetime.strptime(pat_find_1[0] + pat_find_1[1], '%Y%m').strftime('%Y-%m')
            elif len(pat_find_1) == 1:
                t = datetime.datetime.strptime(pat_find_1[0],'%Y').strftime('%Y-%m')
            else:
                t = datetime.datetime.strptime(original_time, '%y年%m月').strftime('%Y-%m')
        elif len(original_time) == 10:
            pat_find_2 = re.findall(r'[0-9]+',original_time)
            if len(pat_find_2) == 1:
                t = datetime.datetime.strptime(pat_find_2[0],'%Y').strftime('%Y-%m')
            else:
                t = datetime.datetime.strptime(original_time, '%y年%m月').strftime('%Y-%m')
        elif len(original_time) == 11 or len(original_time) == 12:
            pat_find_3 = re.findall(r'[0-9]+',original_time)
            if len(pat_find_3) == 2:
                t = datetime.datetime.strptime(pat_find_3[0]+'年'+pat_find_3[1]+'月', '%Y年%m月').strftime('%Y-%m')
            else:
                return '0000-00'
        else:
            pat_find_year = re.findall(r'[0-9]+年', original_time)
            pat_find_month = re.findall(r'[0-9]+月', original_time)
            if len(pat_find_year) > 0:
                if len(pat_find_month) > 0:
                    original_time = pat_find_year[0] + pat_find_month[0]
                    if len(original_time) == 9 or len(original_time) == 10:
                        t = datetime.datetime.strptime(original_time, '%y年%m月').strftime('%Y-%m')
                    elif len(original_time) == 11 or len(original_time) == 12:
                        t = datetime.datetime.strptime(original_time, '%Y年%m月').strftime('%Y-%m')
                else:
                    original_time = pat_find_year[0]
                    if len(original_time) == 5:
                        t = datetime.datetime.strptime(original_time, '%y年').strftime('%Y-%m')
                    elif len(original_time) == 7:
                        t = datetime.datetime.strptime(original_time, '%Y年').strftime('%Y-%m')
    elif original_time == '至今':
        t = time.strftime('%Y-%m', time.localtime(time.time()))
    else:
        if len(original_time) == 4:
            pat_find_year_y = re.findall(r'[0-9]{2}', original_time)
            pat_find_year_Y = re.findall(r'[0-9]{4}', original_time)
            if original_time.find('.') != -1:
                t = datetime.datetime.strptime(original_time, '%y.%m').strftime('%Y-%m')
            elif len(pat_find_year_Y) > 0:
                t = datetime.datetime.strptime(pat_find_year_Y[0], '%Y').strftime('%Y-%m')
            elif len(pat_find_year_y) > 0:
                t = datetime.datetime.strptime(pat_find_year_y[0], '%y').strftime('%Y-%m')
            else:
                return '0000-00'
        elif len(original_time) == 5:
            pat_find_year_y = re.findall(r'[0-9]{2}', original_time)
            if original_time.find('-') != -1:
                t = datetime.datetime.strptime(original_time, '%Y-').strftime('%Y-%m')
            elif original_time.endswith('.'):
                t = datetime.datetime.strptime(original_time, '%Y.').strftime('%Y-%m')
            elif original_time.find('.') != -1:
                t = datetime.datetime.strptime(original_time, '%y.%m').strftime('%Y-%m')
            elif original_time.find('/') != -1:
                t = datetime.datetime.strptime(original_time, '%Y/').strftime('%Y-%m')
            elif len(pat_find_year_y) > 0:
                t = datetime.datetime.strptime(pat_find_year_y[0], '%y').strftime('%Y-%m')
            else:
                t = datetime.datetime.strptime(original_time, '%y.%m').strftime('%Y-%m')
        elif len(original_time) == 6:
            pat_find_number = re.findall(r'[0-9]+', original_time)
            if original_time.find('.') != -1:
                if original_time.find('.') == 1:
                    t = datetime.datetime.strptime(original_time,'%m.%Y').strftime('%Y-%m')
                else:
                    t = datetime.datetime.strptime(original_time, '%Y.%m').strftime('%Y-%m')
            elif original_time.find('/') != -1:
                t = datetime.datetime.strptime(original_time, '%Y/%m').strftime('%Y-%m')
            elif original_time.find('--') != -1:
                t = datetime.datetime.strptime(original_time, '%Y--').strftime('%Y-%m')
            elif original_time.find(',') != -1:
                t = datetime.datetime.strptime(original_time, '%Y,%m').strftime('%Y-%m')
            elif len(pat_find_number) == 0:
                return '0000-00'
            else:
                pat_find_4 = re.findall(r'[0-9]+',original_time)
                if len(pat_find_4) != 0:
                    if len(pat_find_4[0]) == 2:
                        t = datetime.datetime.strptime(pat_find_4[0], '%y').strftime('%Y-%m')
                    else:
                        t = datetime.datetime.strptime(original_time, '%Y%m').strftime('%Y-%m')
                else:
                    return '0000-00'
        elif len(original_time) == 7:
            pat_find_year = re.findall(r'[0-9]{4}', original_time)
            if original_time.find('/') != -1:
                t = datetime.datetime.strptime(original_time, '%Y/%m').strftime('%Y-%m')
            elif original_time.find('---') != -1:
                t = datetime.datetime.strptime(original_time, '%Y---').strftime('%Y-%m')
            elif original_time.find(',') != -1:
                t = datetime.datetime.strptime(original_time, '%Y,%m').strftime('%Y-%m')
            elif len(pat_find_year) > 0:
                t = datetime.datetime.strptime(pat_find_year[0], '%Y').strftime('%Y-%m')
            else:
                t = datetime.datetime.strptime(original_time, '%Y.%m').strftime('%Y-%m')
        else:
            pat_find_year = re.findall(r'[0-9]{4}', original_time)
            if len(pat_find_year) > 0:
                original_time = pat_find_year[0]
                t = datetime.datetime.strptime(original_time, '%Y').strftime('%Y-%m')
            else:
                return '0000-00'
    return t


def main():
    usage = """
    format_time.py [options]
    """
    fmt = optparse.IndentedHelpFormatter(max_help_position=50, width=100)
    parser = optparse.OptionParser(usage=usage, formatter=fmt)
    parser.add_option('-i', '--input', help='Input File')
    parser.add_option('-o', '--output', help='Output File')
    parser, args = parser.parse_args()
    if parser.input:
        event_json_read = ReadFile(parser.input)
    event_list = simplejson.loads(event_json_read)
    result = {}
    formatMiss = 0
    for i in range(len(event_list)):
        if len(event_list[i]['start_time']) != 0:
            try:
                event_list[i]['start_time'] = format_time(event_list[i]['start_time'])
            except ValueError, e:
                event_list[i]['start_time'] = '0000-00'
                formatMiss += 1
                print e
        if len(event_list[i]['end_time']) != 0:
            try:
                event_list[i]['end_time'] = format_time(event_list[i]['end_time'])
            except ValueError, e:
                event_list[i]['start_time'] = '0000-00'
                formatMiss += 1
                print e
        if len(event_list[i]['timenode']) != 0:
            try:
                event_list[i]['timenode'] = format_time(event_list[i]['timenode'])
            except ValueError, e:
                event_list[i]['start_time'] = '0000-00'
                formatMiss += 1
                print e
        print str(formatMiss)
    event_json_out_string = ''
    event_json_out_string = simplejson.dumps(event_list)
    with open(parser.output, 'a+') as outputFile:
        outputFile.write(event_json_out_string.decode('unicode-escape').encode('utf-8'))


if __name__ == "__main__":
    main()