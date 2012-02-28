from myApp import app

from flask import render_template

from flask import jsonify
import pymongo

import json

def result(f):
    def show(*args, **kwargs):
        cursor = f()
        res = []
        for c in cursor:
            if "_id" in c: c["_id"] = str(c["_id"])
            res.append(c)
        return json.dumps(res) 
    return show

@app.route("/json")
@result
def json1(): 
    db = pymongo.Connection("127.0.0.1", 27017).app 
    cursor = db.groups.find() 
    return cursor 

@app.route("/api/json")
def getjson():
    return render_template("jd.json")


