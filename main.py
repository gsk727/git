#-*- coding: utf-8 -*-
# new branch
from flask import Flask, Blueprint

v = Blueprint("v", __name__, static_folder="static")
@v.route("/")
def index():
	return "hello world"

app = Flask(__name__)
app.register_blueprint(v)
app.run(host="0.0.0.0", port = 80)

if __name__ == "__main__":
	print "only for test"

