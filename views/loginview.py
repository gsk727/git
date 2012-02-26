#-*-coding:utf-8 -*-
"""
"""
from flask import Blueprint
from flask.views import MethodView
from flask import render_template
from flask import request, session, redirect, url_for
import pymongo
db = pymongo.Connection("127.0.0.1", 27017).app

loginView = Blueprint("LoginView", __name__, static_folder="static", template_folder="templates")

class LoginView(MethodView):
	"""
	request此view会创建此类
	"""
	def __init__(self):
		pass
		
	def get(self):
		return render_template("login.html")
		
	def post(self):
		username, password = request.form["username"], request.form["password"]
		print "==============", username, password
		if db.user.find({"username":username, "password":password}).count() <=0:
			return redirect(url_for(".login"))
		else:
			session.login = True
		return "hello world"

	def put(self):
		pass
	def delete(self):
		pass
		
loginView.add_url_rule("/login", view_func = LoginView.as_view("login"), methods=["GET", "POST", "PUT", "DELETE"])