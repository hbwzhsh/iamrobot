# -*- coding: gbk -*-
__author__ = 'zhuwei'

import jsbeautifier
import simplejson as json
import os
import sys
import optparse
from math import sqrt
import re
from collections import defaultdict
import time
from time import ctime, sleep
import threading
#from utils.utils_thread import myThread

bufferSize = 50000
StartTime = time.clock()
global global_events
global_events = []


def dot_product(v1, v2):
    """Get the dot product of the two vectors.

    if A = [a1, a2, a3] && B = [b1, b2, b3]; then
    dot_product(A, B) == (a1 * b1) + (a2 * b2) + (a3 * b3)
    true

    Input vectors must be the same length.

    """
    return sum(a * b for a, b in zip(v1, v2))


def magnitude(vector):
    """Returns the numerical length / magnitude of the vector."""
    return sqrt(dot_product(vector, vector))


def similarity(v1, v2):
    """Ratio of the dot product & the product of the magnitudes of vectors."""
    return dot_product(v1, v2) / (magnitude(v1) * magnitude(v2))


def word_frequencies(word_vector):
    """What percent of the time does each word in the vector appear?

    Returns a dictionary mapping each word to its frequency.

    """
    num_words = len(word_vector)
    frequencies = defaultdict(float)
    for word in word_vector:
        frequencies[word] += 1.0 / num_words

    return dict(frequencies)


def compare_vectors(word_vector1, word_vector2):
    """Numerical similarity between lists of words. Higher is better.

    Uses cosine similarity.
    Result range: 0 (bad) - 1 (uses all the same words in the same proportions)

    """
    all_words = list(set(word_vector1).union(set(word_vector2)))
    frequency_dict1 = word_frequencies(word_vector1)
    frequency_dict2 = word_frequencies(word_vector2)

    frequency_vector1 = [frequency_dict1.get(word, 0) for word in all_words]
    frequency_vector2 = [frequency_dict2.get(word, 0) for word in all_words]

    return similarity(frequency_vector1, frequency_vector2)


def vectorize_text(text):
    """Takes in text, processes it, and vectorizes it."""

    def remove_punctuation(text):
        """Removes special characters from text."""
        return re.sub('[,.?";:\-!@#$%^&*()]', '', text)

    def remove_common_words(text_vector):
        """Removes 50 most common words in the uk english.

        source: http://www.bckelk.ukfsn.org/words/uk1000n.html

        """
        common_words = set(['the', 'and', 'to', 'of', 'a', 'I', 'in', 'was',
                            'he', 'that', 'it', 'his', 'her', 'you', 'as', 'had', 'with',
                            'for', 'she', 'not', 'at', 'but', 'be', 'my', 'on', 'have', 'him',
                            'is', 'said', 'me', 'which', 'by', 'so', 'this', 'all', 'from',
                            'they', 'no', 'were', 'if', 'would', 'or', 'when', 'what', 'there',
                            'been', 'one', 'could', 'very', 'an', 'who'])
        return [word for word in text_vector if word not in common_words]

    text = text.lower()
    text = remove_punctuation(text)
    words_list = text.split()
    words_list = remove_common_words(words_list)
    return words_list


def compare_texts(text1, text2):
    """How similar are the two input paragraphs?"""
    return compare_vectors(vectorize_text(text1), vectorize_text(text2))


def saving(data, output_filename):
    with open(output_filename, 'a+') as outPutFile:
        outPutFile.write(data + "\n")

def compare_institute(EventList):
    print 'Start time:', \
        ctime()
    result = {}
    for _event in range(len(EventList)):
        print "Current Event" + str(_event)
        EventList[_event]['same_institute'] = ''
        f = EventList[_event]['institute'].strip()
        result['no_institute'] = []
        print f
        if len(f):
            if f in result:
                result[f].append(_event)
            else:
                result[f] = []
                result[f].append(_event)
        else:
            result['no_institute'].append(EventList[_event]['id'])
    print 'End time:', \
        ctime()
    print len(EventList)
    for i in result.keys():
        for j in result[i]:
            print j
            print str(EventList[j]['id'])
            EventList[j]['same_institute'] = result[i]
    print 'End time:', \
        ctime()
    return EventList


def ReadFile(filename):
    print 'Start at:', \
        ctime()
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
    print 'Finish reading at:', \
        ctime()
    return fileS


def cosVector(x, y):
    if (len(x) != len(y)):
        print ('Error! x and y is not in the same space')
        return
    result1 = 0.0
    result2 = 0.0
    result3 = 0.0
    for i in range(len(x)):
        result1 += x[i] * y[i]
        result2 += x[i] ** 2
        result3 += y[i] ** 2
    return result1 / ((result2 * result3) ** 0.5)


def get_similarity(a_string='', b_string=''):
    a_string = a_string.strip()
    b_string = b_string.strip()
    pass


def main():
    usage = """
    get_similar_events.py [options]
    """
    fmt = optparse.IndentedHelpFormatter(max_help_position=50, width=100)
    parser = optparse.OptionParser(usage=usage, formatter=fmt)
    parser.add_option('-i', '--input', help='Input File')
    parser.add_option('-o', '--output', help='Output File')
    parser, args = parser.parse_args()
    fields = ["timenode", "start_time", "end_time", "department", "institute", "event", "title"]
    init_sql = 'INSERT INTO `51prof_main`.`prof_events` (`department`,`end_time`,`event`,`id`,`institute`,`person_id`,`same_institute`,`start_time`,`timenode`,`title`) VALUES (%s, %s, %s, %s, %s, %s , %s, %s,%s,%s)'
    print StartTime
    if parser.input:
        event_json_read = ReadFile(parser.input)
        EventList = json.loads(event_json_read)
        result = compare_institute(EventList)
        for i in result:
            print i['id']
            sql = init_sql % (i['department'].encode('utf-8'),
                              i['end_time'].encode('utf-8'),
                              i['event'].encode('utf-8'),
                              i['id'],
                              i['institute'].encode('utf-8'),
                              i['person_id'],
                              json.dumps(i['same_institute']).decode('unicode-escape').encode('utf-8'),
                              i['start_time'].encode('utf-8'),
                              i['timenode'].encode('utf-8'),
                              i['title'].encode('utf-8'))
            saving(sql, parser.output)
if __name__ == "__main__":
    main()