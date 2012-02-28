#-*- coding:utf-8 -*-
from db import db
# from magazine import Magazine
from flask.views import MethodView

from flask import render_template

class PublishView(MethodView):
    """
    出版相关的视图
    """
    def get(self, pid):
        pass


    def post(self):
        pass

    def put(self, pid):
        pass

    def delete(self, pid):
        pass


class Magazine(MethodView):
    def get(self, mid):
        res = db.magazine.find({"id":mid}, {"_id":0})[0]
        #print res.count()
        return render_template("magazine.html", res = res) 
     
    def post(self):
        pass
    
    def put(self, id):
        pass
    
    def delete(self, mid):
        pass


