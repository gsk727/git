# -*- coding:utf-8 -*-

import pymongo
from pymongo.database import Database 
from const import *

class GameDB(Database):
    def __init__(self):
        conn = pymongo.Connection(LOCALHOST, DBPORT)
        super(GameDB, self).__init__(conn, DBNAME)
 
class GameDBConn(object):
    pass


