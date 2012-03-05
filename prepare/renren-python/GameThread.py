#-*- coding:utf-8 -*-
"""
线程管理模块
"""

import Queue
import threading
import copy

class GameThreadPool(object):
    """
    作为全局变量存在于Global.py中
    """
    maxThreads = 10
    in_queue = Queue.Queue()
    out_queue = Queue.Queue()
    working = [] 
    threads = []
    def __init__(self):
       self.stoped = False 
       pass

    @classmethod
    def reset(cls):
        if hasattr(cls, "_instance"):
            del cls._instance

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    # def initThreads(self):
    #    for i in xrange(0, self.MaxThreads):
    #        t = GameThread(self.in_queue)
    #        self.threads.append(t)

    def appendTask(self, task_method, task_args, callback = None):
        if not self.stoped:
            self.in_queue.put((task_method, task_args, callback))
            needThreadNums  = len(self.working) + self.in_queue.qsize()        
            if needThreadNums > len(self.threads):
                newThread = GameThread(self.in_queue) 
                self.threads.append(newThread)

    def start(self):
        pass

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def endAllThreads(self):
        self.stoped = True
        threads = copy.copy(self.threads)
        for thread in self.working:
            self.in_queue.put(None)

        for thread in threads:
            self.in_queue.put(None)
            thread.join()

class GameThread(threading.Thread):
    THREAD_IDL = 0
    THREAD_WAIT = 1
    THREAD_RUN = 2
    THREAD_RUNING = 3
    THREAD_STOP = 4
    def __init__(self, queue):
        super(GameThread, self).__init__()
        self.status = self.THREAD_IDL
        self._callback = None
        self.queue = queue
        self.finishAndExit = threading.Event()
        #self.setDaemon(True)
        self.start()

    def run(self):
        while True:
            self.status = self.THREAD_RUNING
            GameThreadPool.working.append(self)
            task = self.queue.get() # true default block
            if task is None:
                break;

            task_method, task_args, callback = task # true default block

            task_result = task_method(*task_args)
            if callback is not None:
                ret = callback(task_result)

            del task_method, task_args, callback

            self.status = self.THREAD_IDL
#           self.queue.task_done()
            GameThreadPool.working.remove(self)

        self.status = self.THREAD_STOP
        GameThreadPool.threads.remove(self)

    def getThreadStatus(self):
        return self.status

def callback(result = None):
    print "callback", result

a = 100
def taskFun():
    import time 
    print a
    time.sleep(10)
import time
if __name__ == "__main__":
    g = GameThreadPool()
    g.appendTask(taskFun, (), callback)
    g.appendTask(taskFun, (), callback)

    #g.start()
    g.endAllThreads()
