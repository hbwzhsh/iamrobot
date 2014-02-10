__author__ = 'zhuwei'
import re
import sys
import os
import optparse
import urllib2
from urllib import urlencode
from urllib import unquote
def main():
    usage = """parseShixin.py [options]
    """
    fmt = optparse.IndentedHelpFormatter(max_help_position=50,
                                         width=100)
    parser = optparse.OptionParser(usage=usage, formatter=fmt)

    parser.add_option('-i', '--input',
                      help='Input Filename')
    parser.add_option('-o', '--output',
                      help='Output Filename')

    options, args = parser.parse_args()

    pat = 'query=(.*?) '
    queryList = []
    for line in file(options.input):
        tmpResult = re.findall(pat, line)
        if len(tmpResult) == 1:
            queryString = unquote(tmpResult[0])
            queryList.append(queryString)
    queryListUnique = {}.fromkeys(queryList).keys()
    with open(options.output,'a+') as outputFile:
        for i in range(len(queryListUnique)):
            outputFile.write(queryListUnique[i] + "\n")
    outputFile.close()
if __name__ == "__main__":
    main()