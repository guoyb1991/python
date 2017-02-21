import urllib
import urllib2
import HTMLParser
import urlparse
import cookielib
import string
import re

cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
values = {"userName":"adminTender","pwd":"asdf1234","accountType":"1"}
data = urllib.urlencode(values) 
url = "http://localhost:8080/user/doLogin.html"
request = urllib2.Request(url,data,headers = headers)
response = urllib2.urlopen(request)
print response.read()


fileHandle = open('F:\123.html','w')
url = "http://localhost:8080/member/main.html"
request = urllib2.Request(url,headers = headers)
response = urllib2.urlopen(request)
fileHandle.write(response.read())
fileHandle.close()