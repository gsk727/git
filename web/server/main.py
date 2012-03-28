#!/usr/bin/python
#-*-coding: utf-8 -*-

"""
app.add_url_rule("")
"""

from flask import *
import pymongo
import json
import md5

db = pymongo.Connection("127.0.0.1", 27017).app
app = Flask(__name__)

app.secret_key = "test"

class MongoJEncoder(json.JSONEncoder):
    """
    游标类型转为list,成员是字典类型, id不再在其中
    """
    def default(self, obj):    
        return [row for row in obj]
    
def getMaxID():
    userid = db.userid.find_and_modify(
                             update = {"$inc":{"ids":1}},
                             query = {"name":"user"},
                             upsert = True
                            )
    return userid["ids"]

@app.route("/")
def main():
    return redirect(url_for("get"))

def _checkLogin(username, password):
    res = db.user.find({"username":username, "password":password}, {"_id":0})
    if res.count() == 1:
        return True
    return False

@app.route("/get/", methods=["GET", "POST"])
def get():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        print request.form
        username = request.form["name"]

@app.route("/register", methods=["POST"])
def register():
    usernick = request.form["usernick"]   
    password = request.form["password"]
    username = request.form["username"]
    useremail = request.form["emali"]
    usersex = request.form["sex"]
    if db.user.find({"usernick":usernick}).count() > 0: redirect(url_for("get"))
    db.user.insert({"usernick":usernick, "password":password, "username":username, "useremail":useremail, 
                        "usersex":usersex,
                    })
    
    return redirect(url_for("/get"))
   
def getGroups():
    """
    获取组
    """
    if request.method == "GET":
        return render_template("index.html")
    
    elif request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        print name, password
        if db.user.find({"username":name}).count() > 0:
            return "INVIALID USER NAME"
        userid = getMaxID()
        db.user.insert({"username":name, "password":password, "id":userid})
        return redirect("/get")
    return ""

def getUser(userid):
    d = {"username":1, "password":1} #default
    fields = map(lambda x: d.update({str(x):1}), request.args.get("filed", "").split(","))# 用, 分割     
    d.update({"_id":0})
    userInfo = db.user.find({"id":userid}, d)
    if userInfo.count() == 0:
        return "no existed user"
    return json.dumps(userInfo, cls = MongoJEncoder)


@app.route("/login", methods=["POST", "GET"])
def login():
    if session.get("login", None):
        return "you Have login"

    if request.method == "POST":
        username = request.form["name"]
        password = request.form["password"]
        if not _checkLogin(username, password):
            return redirect(url_for("get"))
        
        session["login"] = True
        return "hello %s"%(username,)
    
    return render_template("login.html")

app.add_url_rule("/groups/", "get_groups", getGroups, methods=["GET", "POST"])
#app.add_url_rule("/groups/<int:userid>", )
app.add_url_rule("/user/<int:userid>", "get_user", getUser, methods=["GET"]) # POST 更好吧

app.run(debug = True)