# -*- coding:utf-8 -*-
"""
"""
import pyamf
import os
import types
import sys

from twisted.internet import protocol
from pyamf.amf3 import ByteArray
from optparse import OptionParser

import Account
from daemon import Daemon
from GameThread import GameThreadPool

version = sys.version_info.major + sys.version_info.minor/10.0

if version >= 2.7 and sys.platform == "linux2":
    from twisted.internet import epollreactor as reactortype
else:
    from twisted.internet import selectreactor as reactortype

class GameGateWay(protocol.Protocol):
    """This is just about the simplest possible protocol"""
    interval = 1.0 # interval in seconds to send the time
    encoding = pyamf.AMF3
    timeout = 300 
    gameService = {
        "Account":Account.Account,
        # "Avatar":Avatar.Avatar()
    }
    
    def __init__(self):
        self.encoder = pyamf.get_encoder(self.encoding)
        self.decoder = pyamf.get_decoder(self.encoding)
        self.stream = self.encoder.stream
        
    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        ba = ByteArray(data)
        pythonObj =  ba.readObject()
        ret = self._gateExec(pythonObj)
        return ret

    def connectionMade(self):
        print "socket connect"
        self.factory.clients[self.transport.fileno()] = {}
        self.fileno = self.transport.fileno()

        self.transport.setTcpNoDelay(True)
        print self.factory.clients
        
    def connectionLost(self, reason):
        print "Lost a client!"
        print self.factory.clients, self.transport.fileno()
        self.factory.clients.pop(self.fileno)
        
    def _gateExec(self, methodAndArgs):
        method, args = methodAndArgs.get("method", ""), methodAndArgs.get("args", "")
        classMethod = self.getClassMethod(method)
        return classMethod(*args)

    def getClassMethod(self, classMethod):
        className, classMethod = classMethod.split(".")
        classInstance = self.gameService.get(className, None)
        if classInstance  is None:
            # raise
            return None
        
        if self.transport.fileno() not in self.factory.clients:
            return
         
        if self.factory.clients[self.transport.fileno()].get(className, None) is None:
            classInstance = classInstance(self)
            self.factory.clients[self.transport.fileno()][className] = classInstance

        classInstance = self.factory.clients[self.transport.fileno()][className]

        if not hasattr(classInstance, classMethod):
            return None
        func = getattr(classInstance, classMethod)
        
        if not isinstance(func, types.MethodType):
            return None

        return func

class GameFactory(protocol.ServerFactory):
    protocol = GameGateWay
    def startFactory(self):
        self.clients = {}

    def stopFactory(self):
       pass

def addOptions():
    parser = OptionParser()
    parser.add_option("-d", "--daemon", help="set server to a backgroup job", action="store_true", dest="daemon")

    # parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")
    return parser

def run(opt):
    """
    要做c++的python的调用，将来启动server后“回调”此处 
    """
    print "starting server"
    p = addOptions()
    try:
        opt = list(opt)
    except:
        pass

    (options, args) = p.parse_args(list(opt))
    if options.daemon == True:
        d = Daemon(run)
        d.start()
    else:
        factory = GameFactory() 
        reactortype.install()
        t = GameThreadPool.instance()
        from twisted.internet import reactor
        reactor.listenTCP(8089, factory)
        # signal only works in main thread donot install signal
        reactor.run( installSignalHandlers=False)

def onServerShutdown():
    print "server shutdown now"
    from twisted.internet import reactor
    t = GameThreadPool.instance()
    t.endAllThreads()
    reactor.stop()
    #sys.exit(0)

def onRecvSigInt(signum, frame):
    onServerShutdown()
    
import signal
signal.signal(signal.SIGINT, signal.SIG_IGN)

if __name__=="__main__":
    # p = addOptions()
    # (options, args) = p.parse_args()
    # if options.daemon == True:
        # d = Daemon(run)
        # d.start()
    # else:
    run(sys.argv[1:])

