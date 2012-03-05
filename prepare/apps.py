#-*- coding:utf-8 -*-
"""
同时有多个app的时候，使用这里
"""
from reader import Reader
from content import Content
appIns = {}  # app 的事例 key 为[app].example.com 中的[app]

class ReadApp(Flask):
    """
    reader APP
    """
    def __init__(self):
        Flask.__init__(self, __name__)

def get_app(name):
    """
    @param:name http://example.com/reader?args=1
    如果没有则创建app
    """ 
    pass


# 次Apps由fcgi使用.定义__call__
class Apps(object):
    def __call__(self, environ, start_response):
        app = get_app(environ["HTTP_HOST"])
        return app(environ, start_response)


