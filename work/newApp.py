from threading import Lock
from flask import Flask, Blueprint
# app = Flask(__name__)
lock = Lock()
btest = Blueprint("btest", __name__)

@btest.route("/")
def sIndex():
    return "sIndex hello"

#@app.route("/")
#def index():
#    return "hello world"

app = Blueprint("app", __name__)
@app.route("/")
def appIndex():
    return "app index"

default = Blueprint("default", __name__)
@default.route("/")
def dindex():
    return "default index"

instance = {}
def create_app(name):
    print name
    if name in instance:
        return instance[name] 

    print __dict__
    app = Flask(__name__)
    b = __dict__.get(name, default) 
    app.register_blueprint(b)
    instance[name] = app
    return app

def make_app(host):
    host = host.split(":")[0]
    sd = host.split(".")[0]
    print host, sd
    with lock:
        app = instance.get(sd, create_app(sd))
         
        return app

    
class Test(object):
    def __call__(self, environ, start_response):
        print environ, start_response
        app = make_app(environ["HTTP_HOST"]) 
        return app(environ, start_response)


application = Test()
