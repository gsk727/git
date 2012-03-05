#-*-coding: utf-8 -*-
#from myApp import app
from myApp import app as application
from flup.server.fcgi import WSGIServer

WSGIServer(application, bindAddress=("127.0.0.1", 5000)).run()
