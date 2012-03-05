# -*- coding:utf-8 -*-
from client import Client
from gamedb import GameDB

class Avatar(object):
    def __init__(self, callback = None, *args, **kwargs):
        self.db = GameDB()
        
        self.userName = kwargs['userName']
        self.password = kwargs['password']
        if callback is not None:
            callback(self)
    
    def backToAccount(self):
    	self.account.avatar2Account()

    def destroy(self):
        pass

    def onDestroy(self):
        pass

