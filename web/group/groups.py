#-*- coding: utf-8 -*-
from flask import Flask
from flask import Session
from flask import g
from flask.views import View
from flask import render_template
from flask import request
from myApp import app
from flask import url_for, redirect, send_file,abort
import json
from db import db
import os

@app.url_defaults
def clientId(endpoint, values):
    """
    url_for 的时候添加?clientid = xxx
    """
    if "clientid" in values or not g.clientid:
        return 
    values["clientid"] = g.clientid

@app.url_value_preprocessor
def get_clientId(endpoint, values):
    clientid = request.args.get("clientid", None)
    if clientid is None:
        print "ClientID is None; default:123"
        clientid = "123"
    g.clientid = clientid 

class Group(View):
    """
    group
    """
    def __init__(self):
        pass


    def dispatch_request(self, name):
        """
        get groups
        """        

        return render_template("group.html", name=name)

app.add_url_rule("/groups/<name>", view_func = Group.as_view("group"))

@app.route("/file/<fname>.<ftype>")
def send_view(fname, ftype):
    
    if os.path.isfile("/home/gsk/%s.%s"%(fname, ftype)):
        return  send_file("/home/gsk/%s.%s"%(fname, ftype))
    else:
      abort(400)


class Groups(View):
    """
    groups
    """
    def __init__(self, name):
        print name
   
    def dispatch_request(self):
        #res = db.groups.find({}, {"name":1, "_id":0}) 
        res = db.groups.find({}, {"_id":0}) # 后台保证数据的正确性
        
        
        print "-------------", url_for("groups")
        resdct = [dict(name=row["name"], groups=row["groups"]) for row in res]          
        # resdct = [dict(name=row)  for row in res]
        # jreturn  json.dumps(resdct)
        return render_template("groups.html", groups = resdct)


@app.route("/get/<groups>_<group>", methods=["POST",])
def showGroups(groups, group):
    print groups, group
    return "asdas"    

#def route(self, rule, **option):
#    def decorate(f):
#       self.add_url_rule(rule, f, option)
#        return f
#    return decorate

@app.route("/get")
def GetGroups():
    return render_template("index.html")

# ap.add_url_rule 会创建Groups这个类
app.add_url_rule("/groups", view_func = Groups.as_view("groups", "name"), methods=["GET", "POST"])



