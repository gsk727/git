#-*-coding:utf-8 -*-
"""
fcgi.py 的WSGIServer部分参数和默认值
WSGIServer.__init__(multithreaded=True, multiprocess=False,..)
Blueprint("base", __name__, url_prefix="/base")
"""
import sys
import re
from flask import render_template, jsonify, render_template_string, Blueprint, request, flash, abort
from flaskext.babel import gettext, lazy_gettext as _
from common import getDB, AppException  # , app_getID
from util import *
from model import BaseModel       # 每个线程一个
from forms.base import BaseAddForm, BaseUpdateForm
from flaskext.babel import gettext, lazy_gettext as _


baseView = Blueprint("base", __name__, url_prefix="/base", template_folder="templates")
db = getDB("app")


@baseView.before_request
@app_verifyUser(power = False)
def base_beforeRequest():
    """
    完成用户授权的检测，根据需要return
    """
    pass


@baseView.route("/")
def get_all():
    """
    获取所有基地的摘要信息
    """
    data = db.base.find({}, {"_id": 0})
    dataType = request.args.get("dataType", None)
    if dataType == "json":
        return jsonify(message=[x.strip() for x in db.base.distinct("name")])

    updateFrm = BaseUpdateForm()
    addFrm = BaseAddForm()
    return render_template(
                    "base/base.html",
                    addURL= url_for("base.add"),
                    updateURL=url_for("base.update"),
                    data=data,
                    updateForm = updateFrm,
                    addForm = addFrm, 
                    checkType="base"
                )


@baseView.route("/add", methods=["POST", ])
@synchronize
def add():
    """添加一个新的基地，
    线程安全，同步函数
    """
    addFrm = BaseAddForm()
    if addFrm.validate_on_submit():
        db.base.insert(addFrm.asDict())
        flash(_(u"添加成功了"), "success")   # 第二个参数与html的class相关

    return render_template("operator/add.html", addForm=addFrm, addURL= url_for("base.add"))


@baseView.route("/<base>")
def get(base):
    """
    查看指定基地的信息
    @param base: 基地的编号， 这个地方应该有权限的检测
    """
    # 正常的请求处理
    regx = re.compile("^%s$"%(base, ), re.IGNORECASE)
    data = db.base.find({"number": regx}, {"_id":0})

    if data.count() == 0:
        flash(u"不存在的基地, 请从下面选择一个", "error")
        return redirect(url_for("base.get_all"))

    session['base'] = base              # 记录用的查看的当前base
    addFrm = BaseAddForm()
    updateFrm = BaseUpdateForm()
    return render_template(
                    "base/base.html",
                    # addURL=url_for("base.add"),
                    updateURL=url_for("base.update"),
                    data=data,
                    updateForm = updateFrm,
                    addForm = addFrm,
                    checkType="base"
                )


@baseView.route("/<base>/<entity>", methods=["GET", ])
def get_entities(base, entity):
    """
    获取某基地下属于实体范畴的信息
    @param entity: 员工，飞机，设备等等
    @return: 跳转到/<entity>/<base>。即 entity.get 函数
    """
    if entity in ("stuff", "airline", "task", "device"):
        return redirect(url_for("%s.get"%(entity, ), base=base))
    else:
        abort(404);

@baseView.route("/<base>/<entity>/<name>")
def get_entity(base, entity, name):
    """
    获取某基地下实体entity下指定<name>的信息
    @param name: entity记录中的key，比如entity是task，那么name应该是taskid 
    """
    bregx = re.compile("^%s$"%(base, ), re.IGNORECASE)
    nregx = re.compile("^" + name + "$", re.IGNORECASE)
    data = None
    if db.base.find({"number":bregx}).count() == 0:
        flash(_u("不存在的基地，请选择"), "error")
    return redirect(url_for("%s.get"))

    if data is not None:
        addURL=".".join((entity, "add"))
        updateURL = ".".join((entity, "update"))
        return render_template("showTable.html",
                        data=data,
                        tableMap=stuffMap,
                        addURL=url_for(addURL),
                        updateURL=url_for(updateURL),
                        checkType=entity,
            )
    return abort(404)


@baseView.route("/", methods=["POST", ])
def update():
    """
      信息的更新, 可以同时更新信息，后面的覆盖前面的。
      为了防止数据的覆盖，每个线程一个BaseModell
      权限说明:需要从session获取用户名字,做身份和权限的验证
    """
    updateFrm = BaseUpdateForm()

    if updateFrm.validate_on_submit():
        base_mode = getModel(BaseModel)
        base_mode.clear()                             # 一直存在的实例.数据需要清理, cache
        base_mode.doc.update(updateFrm.asDict())
        base_mode.query.update({"number": base_mode.number})
        ret = base_mode.update(upsert=False, safe=True)
        if ret["n"] == 0:
            error = u"不存在的记录"
        elif ret["err"]:
            error = str(ret["err"])
        elif ret["updatedExisting"]:            # 这是更新
            error = "update success"
        else:
            error = "insert success"
        flash(_("%s"%(error, )), "error")
    flash("11111111111111111111111111", "error")
    flash("sdasdasdasdasdasdsadasda", "success")
    return render_template("operator/update.html", updateForm=updateFrm, updateURL=url_for("base.update"))
