#-*- coding:utf-8 -*-
"""
职员视图的方法
/stuff/ 获取所有的员工
/stuff/name: 获取制定员工的名字
/stuff/ post :  更新员工
/stuff/add ：添加员工

"""
from bson import binary 
from flask import Blueprint, request
from flask import jsonify, render_template
import re

from flask import redirect, url_for

from flask import g
from mode.stuff import stuffMap, StuffMode
from util import *


stuffView = Blueprint("stuff", __name__, url_prefix="/stuff")


@stuffView.route("/", defaults={"name": None})
@stuffView.route("/<name>", methods=["GET", ])
def get(name):
    """根据职员email吧，获取职员(用户)的详细信息  
        职员和用户，管理员都被看成是用户
    """
    name = name or g.user
    if not name or len(name) == 0:
        return redirect(url_for("base.get"))

    regx = re.compile("^"+name+"$", re.IGNORECASE)
    data = db.user.find({"name": regx}, {"_id": 0, "password": 0})
    return render_template("showTable.html",
                        data=data,
						tableMap=stuffMap,
						addURL="stuff.add",
						updateURL="stuff.update",
                        checkType="stuff",
            )


@stuffView.route("/", methods=["POST", ])
def update():
    """更新存在员工的信息, 可能员工的某些信息不能更新
    """
    m = getMode(StuffMode)
    for k, _ in stuffMap:
        m[k] = request.form.get("name", "").strip() 
    msg = m.update()
    return jsonify(message=msg)


@stuffView.route("/add", methods=["POST", ])
def add():
    """添加员工的信息
        对一些信息做必要的初始化
    """
    sm = getMode(StuffMode)
    for k, _ in stuffMap:
        sm[k] = request.form.get(k, "").strip()

    if sm["status"] is None:  # or status > 1111:
        sm["status"] = "1-在职"   # s

    base = sm["base"]
    if base is None or not db.base.find({"name": base}):
        return jsonify(smessage=u"不存在的基地")

    name, role, begin, end = sm["name"], sm["role"], sm["begin"], sm["end"]
    m.password = binary.Binary(md5.dm5("123456").digest())
    if name is None or len(name) == 0:
        return jsonify(message=u"留下名字")
    elif role is None or len(role) == 0:
        return jsonify(message=u"你的干什么的")
    elif len(end) > 0:
        return jsonify(message="yyyyyyyyyyyyyyyyyyyyyyyyyyyy")
    elif begin is None:                             # 如果客户端需要的时间格式是写死了这里懒得做处理了啊
        begin = tisme.strftime("%sm/%d/%Y")
    else:
        try:
            m, d, y = begin.split("/")              # 格式月日年
            # begin =
        except:
            return jsonify(message="时间格式不对啊")

    err = sm.insert()
    msg = "ok"
    if err == "EXIST":
        # web请求的这个处理, 耐人寻味的dd:
        # 如果返回错误码，客户端先获取错误码对应的内容，如果没有错误
        # 那就白传了这个错误文字，不如直接返回错误字符串
        msg = u"已经不存在的基地不能添加"


    return jsonify(message=msg)
