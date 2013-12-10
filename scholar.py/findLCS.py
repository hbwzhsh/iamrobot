#!/usr/bin/local/ python
#coding=utf-8
# find an LCS (Longest Common Subsequence).
# *public domain*

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def find_lcs_len(s1, s2):
    m = [[0 for x in s2] for y in s1]
    for p1 in range(len(s1)):
        for p2 in range(len(s2)):
            if s1[p1] == s2[p2]:
                if p1 == 0 or p2 == 0:
                    m[p1][p2] = 1
                else:
                    m[p1][p2] = m[p1 - 1][p2 - 1] + 1
            elif m[p1 - 1][p2] < m[p1][p2 - 1]:
                m[p1][p2] = m[p1][p2 - 1]
            else:                             # m[p1][p2-1] < m[p1-1][p2]
                m[p1][p2] = m[p1 - 1][p2]
    return m[-1][-1]

def find_lcs(s1, s2):
    s1 = s1.upper()
    s2 = s2.upper()
    # length table: every element is set to zero.
    # 生成一个所有元素为0的二维list
    m = [[0 for x in s2] for y in s1]
    # direction table: 1st bit for p1, 2nd bit for p2.
    # 生成一个所有元素为None的二维list
    d = [[None for x in s2] for y in s1]
    # we don't have to care about the boundery check.
    # a negative index always gives an intact zero.
    for p1 in range(len(s1)):
        for p2 in range(len(s2)):
            if s1[p1] == s2[p2]:
                if p1 == 0 or p2 == 0:
                    m[p1][p2] = 1
                else:
                    m[p1][p2] = m[p1 - 1][p2 - 1] + 1
                d[p1][p2] = 3                   # 11: decr. p1 and p2
            elif m[p1 - 1][p2] < m[p1][p2 - 1]:
                m[p1][p2] = m[p1][p2 - 1]
                d[p1][p2] = 2                   # 10: decr. p2 only
            else:                             # m[p1][p2-1] < m[p1-1][p2]
                m[p1][p2] = m[p1 - 1][p2]
                d[p1][p2] = 1                   # 01: decr. p1 only
    (p1, p2) = (len(s1) - 1, len(s2) - 1)
    # now we traverse the table in reverse order.
    s = []
    while 1:
        print p1, p2
        c = d[p1][p2]
        if c == 3: s.append(s1[p1])
        if not ((p1 or p2) and m[p1][p2]): break
        if c & 2: p2 -= 1
        if c & 1: p1 -= 1
    s.reverse()
    return ''.join(s).encode('utf-8')


if __name__ == '__main__':
    print find_lcs(u'13S 技术在现代地图学课程中的作用分析矿山测量', u'“3S”技术在现代地图学课程中的作用分析')
    print find_lcs_len(u'13S 技术在现代地图学课程中的作用分析矿山测量', u'“3S”技术在现代地图学课程中的作用分析')