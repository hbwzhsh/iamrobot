# coding=utf-8
import random
import socket
import urllib2
import cookielib
import re
import time
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

re_edu_container = r'<div class="edu-container">.*?</div>'


ERROR = {
        '0':'Can not open the url,checck you net',
        '1':'Creat download dir error',
        '2':'The image links is empty',
        '3':'Download faild',
        '4':'Build soup error,the html is empty',
        '5':'Can not save the image to your disk',
        }

class BrowserBase(object): 
        def __init__(self):
            socket.setdefaulttimeout(20)
        def speak(self,name,content):
            print '[%s]%s' %(name,content)
        def openurl(self,url):
            cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
            self.opener = urllib2.build_opener(cookie_support,urllib2.HTTPHandler)
            urllib2.install_opener(self.opener)
            user_agents = [
                    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                    'Opera/9.25 (Windows NT 5.1; U; en)',
                    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'
                    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
                    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
                    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "]
            agent = random.choice(user_agents)
            self.opener.addheaders = [("User-agent",agent),("Accept","*/*"),('Referer','http://www.google.com')]                                                            
            try:
                res = self.opener.open(url) 
                print "success"
            except Exception,e:
                self.speak(str(e)+url)
                print "ex"
                unprocessurl.append(url)
                #raise Exception
            else:
                return res
def downloadhtml(targeturl,htmlname):
    spider=BrowserBase()
    url = targeturl
    f = spider.openurl(url)
    data = f.read()
    with open(htmlname,'w') as htmlfile:
        htmlfile.write(data)
#get the targeturl to download the htmlpage to analyse the download-url
def gettargetkeywords():
    print "please input you target keywords:"
    targeturl = raw_input()
    return targeturl
def gettargetname():
    print "please input the name to save the target webpage"
    targetname = raw_input()
    return targetname
if __name__=='__main__':
    unprocessurl = []
    print "******************Welcome*******************"
    print "本脚本仅用于爬取hao123大学导航"
    targeturl = "http://www.hao123.com/edu"
    print "请输入初始文件名"
    html_root = raw_input()
    downloadhtml(targeturl, html_root)
    f = open(html_root)
    root_content = f.read()
    p = re.compile(re_edu_container,re.DOTALL)
    # 查找导航主页中包含子导航部分
    results = p.findall(root_content)
    results = results[0].decode('GBK').encode('utf-8')
    
    f.close()
    # 查找导航主页中子导航url
    p = re.compile('href="(.*?)"')
    secondary_results = p.findall(results)
    # 查找省份
    p = re.compile('class="first">(.*?)</td>')
    provinces = p.findall(results)
    for k in range(len(provinces)):
        with open('output/provinces.js','a+') as provincefile:
            provincefile.write('\''+provinces[k]+'\',')
            print '成功保存省份'
    print "请输入保存文件名、保存选项"
    print "请输入保存选项"
    print "******************"
    print "1.仅学校名称"
    print "2.学校名称和网址"
    print "******************"
    savedoptions = raw_input()
    options = savedoptions.split(' ')
    for i in range(len(secondary_results)):
        p = re.compile('htm\/(.*?.htm)')
        second_filename = p.findall(secondary_results[i])
        second_filename = second_filename[0]
        downloadhtml(secondary_results[i],second_filename)
        f = open(second_filename)
        second_content = f.read()
        f.close()
        p = re.compile('<div class="t1 bgg">.*?</div>',re.DOTALL)
        second_results = p.findall(second_content)
        second_results = second_results[0].decode('GBK').encode('utf-8')
        p = re.compile('<td.*?><p.*?>.*?<a href="(.*?)">(.*?)</a>')
        third_results = p.findall(second_results)
        if(len(third_results)>0):
            for m in range(len(third_results)):
                with open('output/'+options[0],'a+') as resultfile:
                    if(options[1] == "1"):
                        resultfile.write('\''+third_results[m][1]+'\',')
                    else:
                        resultfile.write(third_results[m][1]+'@'+third_results[m][0]+'\n')
    print "finish!"
