#-*- coding:utf-8 -*-

from flask.views import View
from myApp import app
from db import db

import json
from flask import render_template

class iMagazine(object):

    def get(self):
        """
        virtual
        """
        pass

    def show(self):
        """
        virtual
        """
        pass

class Magazine(iMagazine):
    def __init__(self):
        pass

    def get(self):
        pass
     
    def show(self):
        pass

class MagazineView(MethodView):
    """
      数据的结构
      db.groups = {name:xxx, groups:[yyyy, yyyx])
      db.magazines  = {group:yyyy, magazines:[{title : xxxx, {1:yyyy}, {2:xxxx} }, ] 
    """
    def dispatch_request(self, group_member, mname = None, page = 0):
        group, member = group_member.split("_", 1)

        print group, member, page, mname
        if mname is None:   # 显示有几本杂志 
            res = db.magazines.find({"group":member}, {"magazines.title":1, "_id":0}) 
        elif mname is not None and page == 0: # 指定页数
            res = db.magazines.find({"group":member,  "magazines":{"$elemMatch":{
                    "title":mname}}}, {"_id": 0})

        elif mname is not None and page != 0: # 显示所有的
            print  {"group":member, "magazines":{"$elemMatch":{"title":mname} }, "magazines.%s"%((page),):{"$exists":1 }}
            res = db.magezines.find_one({"group":member, "magazines":{"$elemMatch":{"title":mname} }, "magazines.%s"%((page),):{"$exists":1 }})
            if res is not None:
                res = res["magezines"][str[page]]
  
        print res
        if not res:
            return ""

        # if res.count() == 0:
        # 测试分页 
        # return json.dumps(list(res))         
        return json.dumps(list(res)) 
       # return render_template("magazine.html", res = res, mname = mname)

app.add_url_rule("/groups/<group_member>/magazine/<clientid>",
    view_func =  MagazineView.as_view("gmagazine"))

app.add_url_rule("/groups/<group_member>/magazine/<mname>/<clientid>",
    view_func =  MagazineView.as_view("gmagazine"))

app.add_url_rule("/groups/<group_member>/magazine/<mname>/<page>",
    view_func =  MagazineView.as_view("gmagazine"))

app.add_url_rule("/groups/<group_member>/<magezine>/<mname>/<page>/<clientid>",
        view_func= MagazineView.as_view("gmagazine"))

