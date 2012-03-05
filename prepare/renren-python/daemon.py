#-*- coding:utf-8 -*-
import os
import sys
import signal

class Daemon(object):
    def __init__(self, run):
        self.run = run
    
    
    def start(self):
        pid = os.fork()

        if pid > 0:
            return

        os.setsid()
        if os.fork():
            sys.exit(0)
        os.umask(0077)
        for fd in range(0, 1024):
            try:
                os.close(fd)
            except OSError:
                pass
        signal.signal(signal.SIGTERM, self.exitTerm)
        os.open("/dev/null", os.O_RDONLY) # STD_IN 
        os.open("/home/gsk/log", os.O_WRONLY|os.O_CREAT|os.O_APPEND) # STD_OUT 
        #os.open("/home/gsk/log", os.O_WRONLY|os.O_CREAT|os.O_APPEND) # STD_OUT 
        os.dup(1)
        self.run()

    def exitTerm(self, signum, frame):
        from twisted.internet import reactor
        reactor.stop()
        sys.exit(1)
