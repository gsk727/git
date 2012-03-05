# -*- coding :utf-8 -*-
import pyamf
import Messager

# def clientWrap(self, method):
    # def callClient(*args):
        # self.call(method, *args)
        # return "asdsad"
    # print "self, method", self, method
    # callClient.method = method
    # callClient.self = self
    # return callClient

class Client(Messager.Message):
    clientMethods = ["onLogin", ]
    encoding = pyamf.AMF3

    def __init__(self, gateway, clientOwner):
        Messager.Message.__init__(self)
        self.gateway = gateway
        self.client = gateway.transport
        self.encoder = pyamf.get_encoder(self.encoding)
        # self.stream = self.encoder.stream
        self.clientOwner = clientOwner

    def __getattr__(self, method):
        if method in self.clientMethods:
            return self.clientWrap(method)
        else:
            raise AttributeError(method)

    def clientWrap(self, method):
        def callClient(*args):
            self.call(method, *args)

        return callClient

    def call(self, method, *args):
        obj = {
            "method":"%s.%s"%(self.clientOwner, method),
            "args":args
        }
        print obj
        #self.encoder.writeElement(obj)
        self.addData("dict", obj)
        self.client.write(self.stream.getvalue())
        self.client.doWrite()
        # self.encoder.context.clear()
        self.reset()
