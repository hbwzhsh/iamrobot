__author__ = 'zhuwei'
# coding=utf-8


import optparse
import re
import sys
import os

re_cite = r'<a href="(/scholar\?cites=.*?)".*?>Cited by (\d*)</a>'
re_author_source = r'<div class="gs_a">((.*?)-(.*?))</div>'

"""
Common functions
"""
def read_file_by_buffer(filename, buffer_size=50000):
    buffer_size = buffer_size
    f = file(filename, 'r')
    string_buffer = f.read(buffer_size)
    total_size = os.path.getsize(filename)
    file_string = ""
    while len(string_buffer):
        file_string += buffer
        f_progress = 100.0 * len(file_string) / total_size
        os.write(1, "\r Progress[%.3f %% (%d/%d)]" % (f_progress, len(file_string), total_size))
        sys.stdout.flush()
        string_buffer = f.read(buffer_size)
    f.close()
    print "\n Read f %s Finished" % filename
    return file_string


def get_cited_info(input_string):

def main():
    usage = """

    """
    fmt = optparse.IndentedHelpFormatter(max_help_position=50,
                                         width=100)
    parser = optparse.OptionParser(usage=usage, formatter=fmt)
    parser.add_option('-i', '--input',
                      help='Input file')
    parser.add_option('-o','--output',
                      help='Output file')
    options = parser.parse_args()

    if not options.input:
        print 'I need an input filename'
        sys.exit(1)
    elif not options.output:
        print 'I need an output filename'
        sys.exit(1)
    else:
        get_cited_info()

if __name__ == "__main__":
    main()