#-*- coding: utf-8 -*-
from flask import Flask
from flask import Session
from flask import g
from flask.views import View
from flask import render_template
from flask import request
from flask import url_for, redirect, send_file,abort
from flask.views import MethodView
import json
from db import db
import os
import pymongo
from flask import Blueprint

from publish import PublishView, Magazine
from jsone import JsonEncoder

groups = Blueprint("groups", __name__, template_folder="../templates")
@groups.before_request
def before_r():
    print "before_request, asdasdasD"

@groups.after_request
def after_r(response):
    # print g.test
    g.test = g.clientid

    return response

# @groups.app_url_defaults 针对的是app
# 大量的这种函数见blueprint.py
@groups.url_defaults # 针对本blueprint的url_defaults
def clientId(endpoint, values):
    """
    url_for 的时候添加?clientid = xxx
    """
    if "clientid" in values or not hasattr(g, "clientid"):
        return 
    
    values["clientid"] = g.clientid

@groups.url_value_preprocessor
def get_clientId(endpoint, values):
    print "url_value_preprocessor"

    clientid = request.args.get("clientid", None)
    if clientid is None:
        clientid = "123"
    g.clientid = clientid 

@groups.errorhandler(404)
def ppap(e):
    return "什么也没有"

class Group(MethodView):
    """
    group
    """
    def get(self, name):
        res = db.groups.find({"name":name}, {"_id":0})
        print url_for(".groups", name="testname")

        if res.count() == 0:
            return "没有"

        mres = db.magazine.find({"gid":res[0]["gid"]}, {"_id":0})

        #return render_template("group.html", mres = mres, gname = name)

        return json.dumps(mres, cls=JsonEncoder)
   
    def post(self):
        gName = request.form.get("name", None)
        if gName is None:
            return "name"
        if db.groups.find({"name":gName}).count() > 0:
            return "exists"

        gid = db.groups.find_and_modify(query = {"name":"groups"}, update ={"$inc":{"gid":1}}, upsert = True)["gid"]

        db.groups.insert({"name":gName, "gid":gid}, False)
        res = db.groups.find({}, {"_id":0}).sort([("gid", pymongo.ASCENDING), ]) 
        return json.dumps([row for row in res])

    def put(self, name):
        pass

    def delete(self, name):
        pass


#    def __init__(self):
#        pass
#
#e
#    def dispatch_request(self, name):
#        """
#        get groups
#        """        
#
#        return render_template("group.html", name=name)


groups.add_url_rule("/groups", "groupPost", view_func = Group.as_view("groupPost"), methods=["POST", ])
groups.add_url_rule("/groups/<name>", view_func = Group.as_view("groups"), methods=["GET", ])

groups.add_url_rule("/groups/publish/<int:pid>", view_func = PublishView.as_view("publish"))

groups.add_url_rule("/publish/<int:id>", view_func = PublishView.as_view("publishview"), methods=["POST", "PUT", "DELETE"])

groups.add_url_rule("/publsih", view_func = PublishView.as_view("publishview"), methods=["GET", ])
#groups.add_url_rule("/magazine", view_func = Magazine.as_view("magazine"), methods= ["GET",])
groups.add_url_rule("/magazine/<int:mid>", view_func = Magazine.as_view("magazine"), methods= ["POST", "PUT", "DELETE", "GET"])


@groups.route("/file/<fname>.<ftype>")
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
                
        
        print "-------------i1111111111111", url_for("groups.groups")
        resdct = [dict(name=row["name"], groups=row["groups"]) for row in res]          
        # resdct = [dict(name=row)  for row in res]
        # jreturn  json.dumps(resdct)
        return render_template("groups.html", groups = resdct)


@groups.route("/get/<groups>_<group>", methods=["POST",])
def showGroups(groups, group):
    print groups, group
    return "asdas"    

#def route(self, rule, **option):
#    def decorate(f):
#       self.add_url_rule(rule, f, option)
#        return f
#    return decorate

@groups.route("/get")
def GetGroups():
    return render_template("index.html")

@groups.route("/groups/<gname>/create_topic", methods=["POST",])
def create_topic(gname):
    print "------------------------------", gname
    res =  db.groups.find({"name":gname})    
    if res.count() == 0:
        return "1111"
    
    title = request.form["title"]
    db.magazine.insert({"gid":res[0]["gid"], "title":title, "id":1000}) 
    return "12312321"

# ap.add_url_rule 会创建Groups这个类
# groups.add_url_rule("/groups", view_func = Groups.as_view("groups", "name"), methods=["GET", "POST"])




