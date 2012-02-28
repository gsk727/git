#-*- coding:utf-8 -*-
from db import db
from magazine import Magazine

class PublishView(object):
    """
    出版相关的视图
    """
    def __init__(self):
        pass

    def dispatch_request(self, group, publish):
        """
        /<group>/<publis>
        """
        result = db.group.findOne({"name":group, "publish":{"$in": [publish,]}})
        if result is None:
            redirect(url_for("index"))


class Publish(object):
    """
    有好多的杂志
    """
    def __init__(self):
       self.__cache = []

    def getMagezine(self, name):
        res = db.publish.find({"name":name})        
        if res.count() == 0:
            return None
        else:            
            self.__cache.append( Magazine(name))  # ...


