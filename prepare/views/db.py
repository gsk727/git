#-*-coding:utf-8 -*-
import pymongo

try:
    _Conn = pymongo.Connection("192.168.1.109", 27017)
    DB = _Conn.reader
except pymongo.errors.AutoReconnect, des:
    #_Conn.close()
    raise Exception(str(des)+", may db do not start")

