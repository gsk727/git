# -*- coding:utf-8 -*-

from gamedb import GameDB
from client import Client
from Avatar import Avatar
import functools
import GameThread
import os

class Account(object):
    def __init__(self, gateway):
        self.db = GameDB()
        self.gt  = GameThread.GameThreadPool.instance()
        
        self.client = Client(gateway, self.__class__.__name__)
        self.isLogined = False

    def login(self, userName, password):
        def callback(userInfo, userName):
            if userInfo is None:
                self.client.onLogin(False, 0x0202)
                return "login out"

            return self.createAvatar(userInfo)
         
        if self.isLogined:
            print "has Logined"
            self.client.onLogin(False, 0x0201)
            return

        cb = functools.partial(callback, userName = userName)
        self.gt.appendTask(self.db.user.find_one, ({"userName":userName, "password":password}, {'_id':0},), cb)
        return
 
    def createAvatar(self, avatarInfo):
        def onCreateAvatar(avatar):
            print "onCreateAvatar", avatar.userName
            self.isLogined = True
            self.avatar = avatar
            self.client.onLogin(True, 0, avatarInfo)
            
        Avatar(onCreateAvatar, **avatarInfo)
        return
    
    def onAvatar2Account(self):
	    self.avatar.destroy()
	    self.avatar = None
   
   

    

