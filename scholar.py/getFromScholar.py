#! /usr/bin/env python
#coding=utf-8
"""
This module provides classes for querying Google Scholar and parsing
returned results.  It currently *only* processes the first results
page.  It is not a recursive crawler.
"""
# Version: 1.5 -- $Date: 2012-09-27 10:44:39 -0700 (Thu, 27 Sep 2012) $
#
# ChangeLog
# ---------
#
# 1.6:  Cookie support, from Matej Smid (https://github.com/palmstrom).
#
# 1.5:  A few changes:
#
#       - Tweak suggested by Tobias Isenberg: use unicode during CSV
#         formatting.
#
#       - The option -c|--count now understands numbers up to 100 as
#         well. Likewise suggested by Tobias.
#
#       - By default, text rendering mode is now active. This avoids
#         confusion when playing with the script, as it used to report
#         nothing when the user didn't select an explicit output mode.
#
# 1.4:  Updates to reflect changes in Scholar's page rendering,
#       contributed by Amanda Hay at Tufts -- thanks!
#
# 1.3:  Updates to reflect changes in Scholar's page rendering.
#
# 1.2:  Minor tweaks, mostly thanks to helpful feedback from Dan Bolser.
#       Thanks Dan!
#
# 1.1:  Made author field explicit, added --author option.
#
# pylint: disable-msg=C0111
#
# Copyright 2010--2013 Christian Kreibich. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
import httplib
import socket
import hashlib
import optparse
import sys
import re
import random
import urllib
import urllib2
import time
from xml.sax import handler, parseString
import os
from BeautifulSoup import BeautifulSoup
import simplejson
from cookielib import CookieJar
#import gscholar

global user_agents

user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]
proxyFile = file(sys.argv[2], 'r')
proxy_list = []
for i in proxyFile.readlines():
    proxy_list.append(i.strip())


def ReadFile(filename):
    global bufferSize
    bufferSize = 50000
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


class Article():
    """
    A class representing articles listed on Google Scholar.  The class
    provides basic dictionary-like behavior.
    """

    def __init__(self):
        self.attrs = {'title': [None, 'Title', 0],
                      'url': [None, 'URL', 1],
                      'num_citations': [0, 'Citations', 2],
                      'num_versions': [0, 'Versions', 3],
                      'url_citations': [None, 'Citations list', 4],
                      'url_versions': [None, 'Versions list', 5],
                      'year': [None, 'Year', 6]}

    def __getitem__(self, key):
        if key in self.attrs:
            return self.attrs[key][0]
        return None

    def __setitem__(self, key, item):
        if key in self.attrs:
            self.attrs[key][0] = item
        else:
            self.attrs[key] = [item, key, len(self.attrs)]

    def __delitem__(self, key):
        if key in self.attrs:
            del self.attrs[key]

    def as_txt(self):
        # Get items sorted in specified order:
        items = sorted(self.attrs.values(), key=lambda item: item[2])
        # Find largest label length:
        max_label_len = max([len(str(item[1])) for item in items])
        fmt = '%%%ds %%s' % max_label_len
        return '\n'.join([fmt % (item[1], item[0]) for item in items])

    def as_csv(self, header=False, sep='|'):
        # Get keys sorted in specified order:
        keys = [pair[0] for pair in \
                sorted([(key, val[2]) for key, val in self.attrs.items()],
                       key=lambda pair: pair[1])]
        res = []
        if header:
            res.append(sep.join(keys))
        res.append(sep.join([unicode(self.attrs[key][0]) for key in keys]))
        return '\n'.join(res)


class ScholarParser():
    """
    ScholarParser can parse HTML document strings obtained from Google
    Scholar. It invokes the handle_article() callback on each article
    that was parsed successfully.
    """
    SCHOLAR_SITE = 'http://scholar.google.com'

    def __init__(self, site=None):
        self.soup = None
        self.article = None
        self.site = site or self.SCHOLAR_SITE
        self.year_re = re.compile(r'\b(?:20|19)\d{2}\b')

    def handle_article(self, art):
        """
        In this base class, the callback does nothing.
        """

    def parse(self, html):
        """
        This method initiates parsing of HTML content.
        """
        self.soup = BeautifulSoup(html)
        for div in self.soup.findAll(ScholarParser._tag_checker):
            self._parse_article(div)

    def _parse_article(self, div):
        self.article = Article()

        for tag in div:
            if not hasattr(tag, 'name'):
                continue

            if tag.name == 'div' and tag.get('class') == 'gs_rt' and \
                    tag.h3 and tag.h3.a:
                self.article['title'] = ''.join(tag.h3.a.findAll(text=True))
                self.article['url'] = self._path2url(tag.h3.a['href'])

            if tag.name == 'font':
                for tag2 in tag:
                    if not hasattr(tag2, 'name'):
                        continue
                    if tag2.name == 'span' and tag2.get('class') == 'gs_fl':
                        self._parse_links(tag2)

        if self.article['title']:
            self.handle_article(self.article)

    def _parse_links(self, span):
        for tag in span:
            if not hasattr(tag, 'name'):
                continue
            if tag.name != 'a' or None == tag.get('href'):
                continue

            if tag.get('href').startswith('/scholar?cites'):
                if hasattr(tag, 'string') and tag.string.startswith('Cited by'):
                    self.article['num_citations'] = \
                        self._as_int(tag.string.split()[-1])
                self.article['url_citations'] = self._path2url(tag.get('href'))

            if tag.get('href').startswith('/scholar?cluster'):
                if hasattr(tag, 'string') and tag.string.startswith('All '):
                    self.article['num_versions'] = \
                        self._as_int(tag.string.split()[1])
                self.article['url_versions'] = self._path2url(tag.get('href'))

    @staticmethod
    def _tag_checker(tag):
        if tag.name == 'div' and tag.get('class') == 'gs_r':
            return True
        return False

    @staticmethod
    def _as_int(obj):
        try:
            return int(obj)
        except ValueError:
            return None

    def _path2url(self, path):
        if path.startswith('http://'):
            return path
        if not path.startswith('/'):
            path = '/' + path
        return self.site + path


class ScholarParser120201(ScholarParser):
    """
    This class reflects update to the Scholar results page layout that
    Google recently.
    """

    def _parse_article(self, div):
        self.article = Article()

        for tag in div:
            if not hasattr(tag, 'name'):
                continue
            if tag.name == 'h3' and tag.get('class') == 'gs_rt' and tag.a:
                self.article['title'] = ''.join(tag.a.findAll(text=True))
                self.article['url'] = self._path2url(tag.a['href'])

            if tag.name == 'div' and tag.get('class') == 'gs_a':
                year = self.year_re.findall(tag.text)
                self.article['year'] = year[0] if len(year) > 0 else None

            if tag.name == 'div' and tag.get('class') == 'gs_fl':
                self._parse_links(tag)

        if self.article['title']:
            self.handle_article(self.article)


class ScholarParser120726(ScholarParser):
    """
    This class reflects update to the Scholar results page layout that
    Google made 07/26/12.
    """

    def _parse_article(self, div):
        self.article = Article()

        for tag in div:
            if not hasattr(tag, 'name'):
                continue

            if tag.name == 'div' and tag.get('class') == 'gs_ri':
                if tag.a:
                    self.article['title'] = ''.join(tag.a.findAll(text=True))
                    self.article['url'] = self._path2url(tag.a['href'])

                if tag.find('div', {'class': 'gs_a'}):
                    year = self.year_re.findall(tag.find('div', {'class': 'gs_a'}).text)
                    self.article['year'] = year[0] if len(year) > 0 else None

                if tag.find('div', {'class': 'gs_fl'}):
                    self._parse_links(tag.find('div', {'class': 'gs_fl'}))

        if self.article['title']:
            self.handle_article(self.article)


class ScholarQuerier():
    """
    ScholarQuerier instances can conduct a search on Google Scholar
    with subsequent parsing of the resulting HTML content.  The
    articles found are collected in the articles member, a list of
    Article instances.
    """
    global user_agents
    SCHOLAR_URL = 'http://scholar.google.com/scholar?hl=en&q=%(query)s+author:%(author)s&btnG=Search&as_subj=eng&as_sdt=1,5&as_ylo=&as_vis=0'
    NOAUTH_URL = 'http://scholar.google.com/scholar?hl=en&q=%(query)s&btnG=Search&as_subj=eng&as_std=1,5&as_ylo=&as_vis=0'

    """
    Older URLs:
    http://scholar.google.com/scholar?q=%s&hl=en&btnG=Search&as_sdt=2001&as_sdtp=on
    """
    user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
    ]

    #UA = 'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.9.2.9) Gecko/20100913 Firefox/3.6.9'

    class Parser(ScholarParser120726):
        def __init__(self, querier):
            ScholarParser.__init__(self)
            self.querier = querier

        def handle_article(self, art):
            self.querier.add_article(art)

    def __init__(self, author='', scholar_url=None, count=0):
        self.articles = []
        self.author = author
        # Clip to 100, as Google doesn't support more anyway
        self.count = min(count, 100)
        self.user_agents = user_agents
        if author == '':
            self.scholar_url = self.NOAUTH_URL
        else:
            self.scholar_url = scholar_url or self.SCHOLAR_URL

        if self.count != 0:
            self.scholar_url += '&num=%d' % self.count
        self.cjar = CookieJar()
        self.proxy = urllib2.ProxyHandler({'http': random.choice(proxy_list)})
        self.proxy_addr = ''
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cjar), self.proxy)

    def query(self, search):
        """
        This method initiates a query with subsequent parsing of the
        response.
        """
        self.clear_articles()
        url = self.scholar_url % {'query': urllib.quote(search.encode('utf-8')), 'author': urllib.quote(self.author)}
        for proxy_addr_ in proxy_list:
            try:
                self.proxy_addr = proxy_addr_
                self.proxy = urllib2.ProxyHandler({'http': self.proxy_addr})
                self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cjar), self.proxy)
                urllib2.install_opener(self.opener)
                req = urllib2.Request(url=url,
                                      headers={'User-Agent': random.choice(self.user_agents)})
                hdl = urllib2.urlopen(req, timeout=20)
                html = hdl.read()
                print self.proxy_addr + 'Success'
                break
            except (urllib2.URLError, httplib.BadStatusLine, socket.error), e:
                if hasattr(e, 'code'):
                    print str(e.code) + e.msg
                    if e.code == 403 or e.code == 503:
                        proxy_list.remove(self.proxy_addr)
                elif hasattr(e, 'reason') and e.reason.message == 'timed out':
                    print "Timed Out" + self.proxy_addr
                    #proxy_list.remove(self.proxy_addr)
                self.proxy_addr = proxy_addr_
                continue
        if not html:
            self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cjar))
            urllib2.install_opener(self.opener)
            try:
                req = urllib2.Request(url=url,
                                      headers={'User-Agent': random.choice(self.user_agents)})
                hdl = urllib2.urlopen(req, timeout=20)
                html = hdl.read()
                print 'Use local network Success'
            except UnboundLocalError, e:
                print str(e)
        self.parse(html)
        with open('/sdc/zhuwei/prof_data/gscholar_html/' + hashlib.new('sha1', url).hexdigest(), 'w') as saved_file:
            saved_file.write(html)

    def parse(self, html):
        """
        This method allows parsing of existing HTML content.
        """
        parser = self.Parser(self)
        parser.parse(html)

    def add_article(self, art):
        self.articles.append(art)

    def clear_articles(self):
        """Clears any existing articles stored from previous queries."""
        self.articles = []


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
    #先将所有字符转换成大写
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


def txt(query, author, count):
    querier = ScholarQuerier(author=author, count=count)
    querier.query(query)
    articles = querier.articles
    if count > 0:
        articles = articles[:count]
    for art in articles:
        print art.as_txt() + '\n'


def saveTxt(query, author, count, personid, paperid):
    querier = ScholarQuerier(author=author, count=count)
    print query
    querier.query(query)
    articles = querier.articles
    if count > 0:
        articles = articles[:count]
    with open(sys.argv[3], 'a+') as papaerFile:
        for art in articles:
            tmp = {}
            tmp[personid] = art.attrs
            tmp["query"] = query
            papaerFile.write(simplejson.dumps(tmp).decode('unicode-escape').encode('utf-8') + '\n')
    papaerFile.close()


def csv(query, author, count, header=False, sep='|'):
    querier = ScholarQuerier(author=author, count=count)
    querier.query(query)
    articles = querier.articles
    if count > 0:
        articles = articles[:count]
    for art in articles:
        result = art.as_csv(header=header, sep=sep)
        print result.encode('utf-8')
        header = False


def url(title, author):
    querier = ScholarQuerier(author=author)
    querier.query(title)
    articles = querier.articles
    for article in articles:
        if "".join(title.lower().split()) == "".join(article['title'].lower().split()):
            return article['url'], article['year']
    return None, None


def titles(author):
    querier = ScholarQuerier(author=author)
    querier.query('')
    articles = querier.articles
    titles = []
    for article in articles:
        titles.append(article['title'])
    return titles


def getand():
    randType = random.randint(1, 10)
    if randType == 1:
        ran = random.randint(5, 10)
    elif randType == 2:
        ran = random.randint(10, 20)
    elif randType == 7:
        ran = random.expovariate(1 / 3.0)
    elif randType == 8:
        ran = random.expovariate(1 / 5.0)
    # Uncomment next tew line to get a larger random number
    #elif randType == 11:
    #    ran = random.expovariate(1 / 100.0)
    else:
        ran = random.randint(1, 3)
    return ran


class PaperHandler(handler.ContentHandler):
    def __init__(self):
        self.doc = {}
        self.current_tag = ""
        self.current_attr = ""
        self.in_quote = 0
        self.count = 1

    def startElement(self, name, attr):
        if name == "table":
            self.doc = {}
        if name == "column":
            self.current_attr = attr['name']
        self.current_tag = name
        self.in_quote = 1

    def endElement(self, name):
        if name == "table":
            if self.doc.get('title', '') <> "":
                in_fields = tuple(self.doc.get(i, '') for i in fields)
                pat = re.compile(u'[\u4e00-\u9fa5]')
                if not re.search(u'[\u4e00-\u9fa5]', in_fields[1]):
                    saveTxt(in_fields[1], author='', count=5, personid=in_fields[5], paperid=in_fields[0])
                    time.sleep(getand())
                print in_fields[1]
                self.count += 1
                sys.stdout.write("\r%.3f%% Finished %s \n" % (
                    100.0 * self.count / 1480365, ('%%-%ds' % 100) % (100 * self.count / 1480365 * '=')))
                sys.stdout.flush()
        self.in_quote = 0

    def characters(self, content):
        if self.in_quote:
            self.doc.update({self.current_attr: content})


def main():
    usage = """scholar.py [options] <query string>
A command-line interface to Google Scholar."""

    fmt = optparse.IndentedHelpFormatter(max_help_position=50,
                                         width=100)
    parser = optparse.OptionParser(usage=usage, formatter=fmt)
    parser.add_option('-a', '--author',
                      help='Author name')
    parser.add_option('-i', '--input',
                      help='Paper List')
    parser.add_option('-o', '--output',
                      help='Output dir')
    parser.add_option('--csv', action='store_true',
                      help='Print article data in CSV format (separator is "|")')
    parser.add_option('--csv-header', action='store_true',
                      help='Like --csv, but print header line with column names')
    parser.add_option('--txt', action='store_true',
                      help='Print article data in text format')
    parser.add_option('-c', '--count', type='int',
                      help='Maximum number of results')
    parser.add_option('-s', '--save', action='store_true',
                      help='Save qquery result in text file')
    parser.set_defaults(count=0, author='')
    options, args = parser.parse_args()

    if len(args) == 0:
        print 'Hrrrm. I  need a query string.'
        sys.exit(1)

    query = ' '.join(args)

    if options.csv:
        csv(query, author=options.author, count=options.count)
    elif options.csv_header:
        csv(query, author=options.author, count=options.count, header=True)
    elif options.save:
        parseString(ReadFile(sys.argv[1]), PaperHandler())
    else:
        txt(query, author=options.author, count=options.count)


if __name__ == "__main__":
    fields = ("id", "title", "source", "time", "authors", "personid")
    main()