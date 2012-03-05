# encoding: utf-8
from reader import Reader
from flup.server.fcgi import WSGIServer

WSGIServer(Reader, bindAddress=("192.168.1.107", 5000)).run()
