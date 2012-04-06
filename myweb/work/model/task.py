#-*- coding:utf-8 -*-
"""
"""
from model import Model

class TaskModel(Model):
    _cName = "task"
    database = "app"
    attributes = ["number", "name", "des", "createDate", "begin", "end", "status",
                        "owner", "history"]

    def __init__(self):
        super(TaskModel, self).__init__()

