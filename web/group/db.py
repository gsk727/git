#-*-coding: utf-8 -*-
import pymongo
# class MongoDB(Pymongo.Connection)
from myApp import app

class MongoDB(object):
    def __init__(self):
        """
        简单的db类
        """
        self.conn = pymongo.Connection("127.0.0.1", 27017)
        self.db = self.conn["app"] 

    @classmethod
    def instance(cls):
        """
        简单的单件模式
        """
        if not hasattr(cls, "_ins"):
            cls._ins = cls()
        return cls._ins

    def close(self):
        self.conn.close()

    def reset(self):
        pass
    
    def GetGroupData(self):
        pass

class GroupData(object):
    name = ""


    
db = MongoDB().instance().db

@app.before_request
def before_request():
    pass

