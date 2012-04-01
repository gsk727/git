#-*- coding:utf-8 -*-
import re
import time

from flask import Blueprint, render_template, request, jsonify, url_for, flash
from flaskext.babel import gettext, lazy_gettext as _
from common import getDB
from util import getMode
from forms.task import TaskAddForm, TaskUpdateForm, TaskShow
from mode import TaskMode


db = getDB("app")
taskView = Blueprint("task", __name__, url_prefix="/task")


@taskView.route("/", methods=["GET", ], defaults={"base": None})
@taskView.route("/<base>")
def get(base):
    """
    获取所有的task,所制定base的的
    """
    addFrm = TaskAddForm()
    updateFrm = TaskUpdateForm()

    if base is None:
        data = db.task.find()
    else:
        data = db.task.find({"base": base})

    return render_template("task.html",
                        data=data,
                        taskShow = TaskShow(addFrm),
                        addForm=addFrm,
                        addURL=url_for("task.add", base=base),
                        updateForm=updateFrm,
                        updateURL=url_for("task.update"),
                        checkType="task",
                        base = base
            )

@taskView.route("/<base>/<taskid>")
def get_task(base, taskid):
    addFrm = TaskAddForm()
    updateFrm = TaskUpdateForm()
    data = db.task.find_one({"number": taskid}, {"_id": 0})
    stuff = {}
    if data is None:
        flash(_u("不存在的任务，刷新再试一试，也许该任务已经被删除"), "error")
    else:
        stuff = db.user.find({}, {"_id":0, "email":1, "name":1})

    return render_template("task_show.html",
                        data=data,
                        taskShow = TaskShow(addFrm),
                        addForm=addFrm,
                        addURL=url_for("task.add", base=base),
                        updateForm=updateFrm,
                        updateURL=url_for("task.update"),
                        checkType="task_show",
                        stuff=stuff,
                        submitUrl = url_for("task.get", base=base, taskid = taskid)
                        
            )


@taskView.route("/", methods=["POST", ])
def update():
    base = request.form.get("base", "").strip()
    stuffID = request.form.get("stuffID", "").strip()
    start = request.form.get("start", "").strip()
    end = request.form.get("end", "").strip()
    fromTime = request.form.get("fromTime", "").strip()
    toTime = request.form.get("toTime", "").strip()
    des = request.form.get("des", "").strip()
    taskID = request.form.get("taskID", "").strip()
    status = request.form.get("status", "").strip()

    regx = re.compile("^%s$" % (stuffID,), re.IGNORECASE)
    if not db.user.find_one({"stuffID": regx}):
        return jsonify(message=u"不存在的员工")

    regx = re.compile("^%s$" % (base,), re.IGNORECASE)
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


@taskView.route("/<base>/add", methods=["POST", ])
def add(base):
    addFrm = TaskAddForm()
    regx = re.compile("^%s$" % (base,), re.IGNORECASE)
    if not db.base.find_one({"number": regx}):
        flash(_(u"不存在的基地"), "error")
    elif addFrm.validate_on_submit():
        tm = getMode(TaskMode)
        tm.doc.update(addFrm.asDict())
        tm.doc.update({"base": base})
        tm.insert()
        print tm.collection
        flash(_(u"总算成功了啊"), "success")

    return render_template("add.html", addForm = addFrm, addURL = url_for("task.add", base=base))

