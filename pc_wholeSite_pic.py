# -*- coding: utf-8 -*-
# ---------------------------------------
import urllib
import urllib2
import cookielib
import re

class PcUtil(object):
    def __init__(self,loginUrl,indexUrl,values):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        self.loginUrl = loginUrl
        self.indexUrl = indexUrl
        self.values = values
        self.x = 0
        self.visitedUrlList = [] # 已经访问过的链接
        self.visitedImgList = [] # 已经保存过的图片
        self.allUrlList = [] # 该站的所有可访问链接

    def login(self):
        cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

        data = urllib.urlencode(self.values)
        request = urllib2.Request(self.loginUrl, data, headers=self.headers)
        response = urllib2.urlopen(request)
        print response.read()

    def getHtml(self,url):

        if url.startswith("/"):
            url = self.indexUrl + url

        #对比已经访问过的url，如果已经访问则结束方法
        for visitedUrl in self.visitedUrlList:
            if visitedUrl == url:
                return None

        print "url:" + url
        request = urllib2.Request(url, None, headers=self.headers)
        try:
            page = urllib2.urlopen(request)  #urllib.urlopen()方法用于打开一个URL地址
        except Exception, e:
            print "出错了"
            self.visitedUrlList.append(url)
            return None
        html = page.read() #read()方法用于读取URL上的数据
        self.visitedUrlList.append(url)
        return html

    def getImg(self,html):
        reg = "<img[^>]*src\s*=\s*\"([^\"]*)\"[^>]*>"    #正则表达式，得到图片地址
        imgre = re.compile(reg)     #re.compile() 可以把正则表达式编译成一个正则表达式对象.
        imglist = re.findall(imgre,html)      #re.findall() 方法读取html 中包含 imgre（正则表达式）的    数据

        #把筛选的图片地址通过for循环遍历并保存到本地
        #核心是urllib.urlretrieve()方法,直接将远程数据下载到本地，图片通过x依次递增命名
        for imgurl in imglist:

            if imgurl.startswith("/"):
                imgurl = self.indexUrl + imgurl

            # 如果已经保存过图片则跳出本次循环，不保存图片
            visited = False
            for visitedImg in self.visitedImgList:
                if visitedImg == imgurl:
                    visited = True
                    break
            if visited:
                continue

            # print imgurl
            try:
                urllib.urlretrieve(imgurl,'E:\pic\python\%s.jpg' % self.x)
            except Exception, e:
                self.visitedImgList.append(imgurl)
                print "错误的图片地址：" + imgurl
            self.x+=1
            self.visitedImgList.append(imgurl)

    def getUrl(self,html):
        reg = "<a[\\s\\S]*?href[\\s]*=[\\s]*[\"|']([\\s\\S]*?)[\"|']"
        regObject = re.compile(reg)
        urlList = re.findall(regObject,html)
        newUrlList = []
        #删除非本站的url
        for url in urlList:
            if url.strip() == "" or (url.startswith("http") and self.indexUrl not in url) or not url.startswith("/"):
                pass
            else:
                newUrlList.append(url)
        return newUrlList


values = {"userName": "adminTender", "pwd": "asdf1234", "accountType": "1"}
loginUrl = "http://localhost:8080/user/doLogin.html"
indexUrl = "http://localhost:8080/"


url = loginUrl
pcUtil = PcUtil(loginUrl, "http://localhost:8080", values)
# pcUtil.login()
urlList = [indexUrl]
hasNew = True
while hasNew:
    isFirst = True # 用来控制第一次循环的时候清空urlList
    hasNew = False # 本次循环是否有未访问页面
    for url in urlList:
        if isFirst:
            urlList = []
            isFirst = False
        html = pcUtil.getHtml(url)
        if html is not None:
            hasNew = True
            # pcUtil.getImg(html)
            urlListPart = pcUtil.getUrl(html)
            urlList.extend(urlListPart)

            # print urlListPart
