#-*- coding:utf-8 -*-
"""
"""
from model import Model


class BaseModel(Model):
    _cName = "base"
    database = "app"
    attributes = ["number", "name", "city", "des"]
    keys = ("name", )
    def __init__(self):
        super(BaseModel, self).__init__()

