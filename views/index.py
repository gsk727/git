#-*- coding:utf-8 -*-

from flask import Blueprint

v = Blueprint("v", __name__, static_folder="static")
@v.route("/")
def index():
	return "hello world"
