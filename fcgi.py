# encoding: utf-8
 
from app import app
from flup.server.fcgi import WSGIServer
 
WSGIServer(app,bindAddress='127.0.0.1:5000').run()
