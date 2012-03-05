#-*- coding:utf-8 -*-
from threading import Thread
from Queue import Queue
import pymongo

import signal


def handler(a, b):
    """
    这个
    """
    print "-========"
    exit(1)


class DBThread(Thread):
    def __init__(self):
        super(DBThread, self).__init__()
        self.__conn = pymongo.Connection()
        self.__db = self.__conn.app

    def run(self, *args, **kwargs):
       while True:
           print self.getName()

class DBThreads(object):
    __threads = []
    work_queue = Queue()

    def __init__(self):
        pass


    def start(self, num = 10):
        for i in xrange(0, num):
            t = DBThread()
            self.__threads.append((t.getName(), t),)
            #t.setDaemon(True)
            t.start()

        self.__num = num

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    DBThreads().start()

