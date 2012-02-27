#!/usr/bin/python
#-*- coding: utf-8 -*-
# new branch
from flask import Flask
from views import index

app = Flask(__name__)
app.register_blueprint(index.v)
app.run(host="0.0.0.0", port = 80)






if __name__ == "__main__":
	print "only for test"

