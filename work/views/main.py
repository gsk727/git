#-*- coding:utf-8 -*-

from flask import render_template
# from myApp import app
from flask import url_for
from flask import request
from db import db
from flask import Blueprint


main = Blueprint("main", __name__, template_folder="../templates")

@main.route("/", methods=['GET', ])
@main.route("/", defaults={"page": 0})
def index():
    """
    主页，显示所有的组
    """    
    print "main -"
    groups = db.groups.find({}, {"_id":0})
    print url_for("groups.groups", name="asd")

    return render_template("index.html", groups = groups)

@main.route("/1users/", defaults={"page": 1})
@main.route("/1users/page/<int:page>")
def show_users(page):
    print "----------------------", request.url
    return str(page)

