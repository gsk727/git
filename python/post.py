#-*- coding: utf-8 -*-
import urllib
import urllib2
import threading
import json

def login():
    post("http://127.0.0.1/user/", 
        {"username":"testA", "password":"123"}
    )


import cookielib
import os

def post(url, data):
    h = {"User-agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:11.0) Gecko/20100101 Firefox/11.0"}

    cj = cookielib.MozillaCookieJar("/home/gsk/git/GIT_GIT/python/cookies.txt")
    #cj = cookielib.CookieJar()
    data = urllib.urlencode(data)  
    print cj
    req=urllib2.Request(url, data, h)
    #response = urllib2.urlopen(req)
    #enable cookie  
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))  
    #urllib2.install_opener(opener)
    response = opener.open(req, data)  
    print "------------------------------"
    return response.read()  


g_count = 0
def run(*args, **kwargs):
    global g_count
    data = {"name":"444a1", "des": str(threading.current_thread().ident)}
    print data
    if g_count%2 == 0:     
        url = "http://127.0.0.1/base/add"
    else:
        url = "http://127.0.0.1/base/"
    g_count+=1

    j = post(url, data)
    if len(j) > 0:
        print json.loads(j)  

import time
if __name__ == "__main__":
    print post("http://www.douban.com/group/topic/28531792/add_comment#last",
        {
            "ck":"ztaG", "rv_comment":"mark", "start":0, "submit_btn":"加上去"
        }
    )
    #login()
    #time.sleep(1) 
    #t = threading.Thread(target=run)
    #t.start() 
    #for i in xrange(0, 200):
    #    t = threading.Thread(target=run)
    #    t.start()

