#-*- coding:utf-8 -*-
"""
"""
from mode import Mode

baseMap = [
    ("number", u"名称"),
    ("name", u"描述"),
    ("city", u"员工"), # 怎么生成一个URL
    ("des", u"描述")
]


class BaseMode(Mode):
    _cName = "base"
    database = "app"
    attributes = baseMap
    keys = ("name", )
    def __init__(self):
        super(BaseMode, self).__init__()

