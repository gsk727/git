#-*- coding:utf-8 -*-

from flask import Blueprint
from flask import render_template, request, jsonify
from common import getDB
import re
import time

db = getDB("app")


taskView = Blueprint("task", __name__, url_prefix="/task")
tableMap = [
             ("base", u"基地"),
             ("stuffID", u"职员ID"),
             ("start", u"开始时间"),
             ("end", u"结束时间"),
             ("fromTime",  u"实际结束时间"),
             ("toTime",  u"实际结束时间"),
             ("diff",  u"实际用时(小时)"),
             ("taskID",  u"任务ID"),
             ("des", u"任务描述")
             ]

dbKeys = []
tHeaders = []

for x in tableMap:
    dbKeys.append(x[0])
    tHeaders.append(x[1])


@taskView.route("/", methods=["GET", ], defaults={"base": None})
@taskView.route("/<base>")
def get(base):
    """
    获取所有的task,所制定base的的
    """
    if base is None:
        data = db.task.find()
    else:
        data = db.task.find({"base": base})

    return render_template("showTable.html",
                        data=data,
						tableMap=tableMap,
						addURL="task.add",
						updateURL="task.update",
                        checkType="task",
            )


@taskView.route("/", methods=["POST", ])
def update():
    #parse_request_form()
    base = request.form.get("base", "").strip()
    stuffID = request.form.get("stuffID", "").strip()
    start = request.form.get("start", "").strip()
    end = request.form.get("end", "").strip()
    fromTime = request.form.get("fromTime", "").strip()
    toTime = request.form.get("toTime", "").strip()
    des = request.form.get("des", "").strip()
    taskID = request.form.get("taskID", "").strip()
    status = request.form.get("status", "").strip()

    regx = re.compile(stuffID, re.IGNORECASE)
    if not db.user.find_one({"stuffID": regx}):
        return jsonify(message=u"不存在的员工")

    regx = re.compile(base, re.IGNORECASE)
    if not db.base.find_one({"base": regx}):
        return jsonify(message=u"不存在的基地")

    if not db.task.find_one({"taskID": taskID}):
        return jsonify(message=u"不存在的任务")

    if start >= end:
        return jsonify(message=u"错误的设定")

    db.task.update({"taskID": taskID},
                   {
                    "base": base,
                    "stuffID": stuffID,
                    "start": start,
                    "end": end,
                    "fromTime": fromTime,
                    "toTime": toTime,
                    "des": des,
                    "status": status,
                    })
    return jsonify(message=u"ok")


@taskView.route("/add", methods=["POST", ])
def add():
    # parse_request_form()
    base = request.form.get("base", "").strip()
    stuffID = request.form.get("stuffID", "").strip()
    start = request.form.get("start", "").strip()
    end = request.form.get("end", "").strip()
    fromTime = request.form.get("fromTime", "").strip()
    toTime = request.form.get("toTime", "").strip()
    des = request.form.get("des", "").strip()
    #status = request.form.get("status", "").strip()
    # taskID = request.form.get("taskID", "").strip()

    status = "free"
    regx = re.compile(base, re.IGNORECASE)
    if not db.base.find_one({"name": regx}):
        return jsonify(message=u"不存在的基地")

    if len(stuffID) != 0:   # 添加任务立即分配
        regx = re.compile(stuffID, re.IGNORECASE)
        if not db.user.find_one({"name": regx}):
            return jsonify(message=u"不存在的员工")
        else:
            status = "running"

    db.task.insert({
                    "base": base,
                    "stuffID": stuffID,
                    "start": start,
                    "end": end,
                    "fromTime": fromTime,
                    "toTime": toTime,
                    "des": des,
                    "status": status,
                    "taskID": int(time.time())
    })

    return jsonify(message="ok")
    
