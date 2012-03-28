#-*- coding:utf-8 -*-
"""
"""
from mode import Mode

baseMap = [
    ("name", u"名称"),
    ("des", u"描述"),
    ("stuff", u"员工"), # 怎么生成一个URL
    
]


class BaseMode(Mode):
    _cName = "base"
    database = "app"
    attributes = baseMap
    keys = ("name", )
    def __init__(self):
        super(BaseMode, self).__init__()

