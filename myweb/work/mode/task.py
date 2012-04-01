#-*- coding:utf-8 -*-
"""
"""
from mode import Mode

class TaskMode(Mode):
    _cName = "task"
    database = "app"
    def __init__(self):
        super(TaskMode, self).__init__()

