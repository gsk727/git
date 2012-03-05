#-*- coding:utf-8 -*-
from flask import Flask, request
from views import PrepareView
from views import ContentView
#from views import db_start
#from views import threadpool

Reader = Flask(__name__)
Reader.register_blueprint(PrepareView)
Reader.register_blueprint(ContentView)

@Reader.route("/test")
def MyIndex():
    from flask import render_template
    return render_template("index.html")

@Reader.route("/test/text", methods=["post",])
def upload():
    filef = request.files["file"]
    filef.save("/home/gsk/u.iso")
    return "ok"


@Reader.teardown_request
def teardown(exception):
    """
    每个request end的时候调用此处
    """
    pass 

if __name__ == "__main__":
 
    Reader.run(debug = True, host="0.0.0.0", port=5000)

