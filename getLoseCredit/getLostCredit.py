# coding = utf-8
__author__ = 'zhuwei'

import sys
import os
import urllib2
import urllib
import optparse
import random
from cookielib import CookieJar
import jsbeautifier
import json


def download(reUrl):
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
    try:
        cjar = CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cjar))
        req = urllib2.Request(url=reUrl, headers={'User-Agent': random.choice(user_agents)})
        urllib2.install_opener(opener)
        hdl = urllib2.urlopen(req, timeout=5)
        html = hdl.read()
        #tmpData = jsbeautifier.beautify(html)
        return html
    except urllib2.URLError, e:
        if hasattr(e, 'code'):
            if e.code == 500:
                return ''


def saveJson(data = '', outputfile = 'output'):
    with open(outputfile, 'a+') as losecredit:
        losecredit.write(data)
    losecredit.close()


def main():
    usage = """ getLostCredit.py [options]
    """
    fmt = optparse.IndentedHelpFormatter(max_help_position=50,
                                         width=100)
    parser = optparse.OptionParser(usage=usage, formatter=fmt)
    parser.add_option('-o', '--output',
                      help='Output file')
    parser.set_defaults(output="loseCredit.json")
    options, args = parser.parse_args()

    #if len(options) == 0:
    #    print 'Hrrrm. I  need a query string.'
    #    sys.exit(1)

    initurl = "http://shixin.court.gov.cn/detail?id="
    id = 2000
    while id <= 50000:
        print id
        data = download(initurl + str(id))
        if data <> '' and data:
            saveJson(data, options.output)
            print data
        id += 1
if __name__ == "__main__":
    main()