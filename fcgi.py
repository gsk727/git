# encoding: utf-8
 
from app import app
from flup.server.fcgi import WSGIServer
 
WSGIServer(app,bindAddress='/home/gsk/source/web/proc.sock').run()