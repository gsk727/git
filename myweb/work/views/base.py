#-*-coding:utf-8 -*-
"""
fcgi.py 的WSGIServer部分参数和默认值
WSGIServer.__init__(multithreaded=True, multiprocess=False,..)
Blueprint("base", __name__, url_prefix="/base")
"""
import re
from flask import render_template, jsonify, render_template_string, Blueprint, request
from flaskext.babel import gettext, lazy_gettext as _
from common import getDB, AppException  # , app_getID
from util import *
from mode.base import baseMap
from mode import BaseMode       # 每个线程一个
from mode.stuff import stuffMap
from forms import base

baseView = Blueprint("base", __name__, url_prefix="/base")
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
    data = db.base.find({}, {"_id": 0})
    dataType = request.args.get("dataType", None)
    if dataType == "json":
        return jsonify(message=[x.strip() for x in db.base.distinct("name")])

    updateFrm = base.BaseUpdateForm()
    addFrm = base.BaseAddForm()
    return render_template(
                    "base.html",
                    addURL="base.add",
                    updateURL="base.update",
                    data=data,
                   updateForm = updateFrm,
                   addForm = addFrm, 
                    #tableMap=baseMap,
                    checkType="base"
                )


@baseView.route("/add", methods=["POST", ])
@synchronize
def add():
    """信息的添加
       锁线程太暴力了。getMode thread_local data
       另外一个方法有木有?
    """
    print "---------------------------------------------, 111111111111111111111111"
    addFrm = base.BaseAddForm()
    if addFrm.validate_on_submit():
        db.base.insert(addFrm.asDict())
        flash(_(u"我靠，终于添加成功了"), "success")   # 第二个参数与html的class相关


    return render_template_string("{% import 'form.html' as forms with context %}\
                <div id='flashed'>\
                        <ul>\
                        {% for category, msg in get_flashed_messages(with_categories=true) %}\
                            <li class='alert alert-{{ category }}'> {{ msg }}</li>\
                        {% endfor %}\
                        </ul>\
                </div>\
                 <div class='span4'>{{ forms.myForm(addForm, addURL) }}</div>", addForm=addFrm, addURL="base.add"
        )

#    data = {}
#    updateFrm = base.BaseUpdateForm()
#    return render_template(
#                    "base.html",
#                    addURL="base.add",
#                    updateURL="base.update",
#                    data=data,
#                   updateForm = updateFrm,
#                   addForm = addFrm, 
#                    #tableMap=baseMap,
#                    checkType="base"
#                )

   # base_mode = getMode(BaseMode)
    #base_mode.name = request.form["name"]
    #base_mode.des = request.form["des"]
   # err = base_mode.insert()                     # 这是一个怪异的操作
   # msg = "ok"
    #if err == "EXIST":
        # web请求的这个处理, 耐人寻味的dd:
        # 如果返回错误码，客户端先获取错误码对应的内容，如果没有错误
        # 那就白传了这个错误文字，不如直接返回错误字符串
      #  msg = u"已经不存在的基地不能添加"

    # time.sleep(10)
    # return jsonify(message=msg)


@baseView.route("/<base>")
def get(base):
    """
    get用户信息的显示, 基地有多个实体, 如果<base> 
    """
    # 正常的请求处理
    regx = re.compile("^%s$"%(base, ), re.IGNORECASE)
    data = db.base.find({"name": regx})
    return render_template(
                    "showTable.html",
                    addURL="base.add",
                    updateURL="base.update",
                    data=data,
                    tableMap=baseMap,
                    checkType="base"
                )


@baseView.route("/<base>/<entity>", methods=["GET", ])
def get_entities(base, entity):
    """
    获取某基地下所有的实体信息
    url:
    """
    regx = re.compile("^%s$"%(base, ), re.IGNORECASE)
    # regx = re.compile(base, re.IGNORECASE)
    data = None
    if entity == "stuff":
        data = db.user.find({"base": regx}, {"_id": 0, "password": 0})
    elif entity == "device":
        data = db.device.find({"base": regx}, {"_id": 0}) 

    if data is not None: 
        addURL=".".join((entity, "add"))
        updateURL = ".".join((entity, "update"))
        return render_template("showTable.html",
                        data=data,
                        tableMap=stuffMap,
                        addURL=addURL,
                        updateURL=updateURL,
                        checkType=entity,
            )
    return abort(404)


@baseView.route("/<base>/<entity>/<name>")
def get_entity(base, entity, name):
    """
    查看制定entity的信息
    """ 
    bregx = re.compile("^%s$"%(base, ), re.IGNORECASE)
    nregx = re.compile("^" + name + "$", re.IGNORECASE) 
    data = None
    if entity == "stuff":
        data = db.user.find({"base": bregx, "name": nregx}, {"_id": 0, "password": 0})
    elif entity == "device":
        data = db.device.find({"base": bregx, "name": nregx}, {"_id": 0}) 
    
    if data is not None: 
        addURL=".".join((entity, "add"))
        updateURL = ".".join((entity, "update"))
        return render_template("showTable.html",
                        data=data,
                        tableMap=stuffMap,
                        addURL=addURL,
                        updateURL=updateURL,
                        checkType=entity,
            )
    
    return abort(404)
 

@baseView.route("/", methods=["POST", ])
def update():
    """
      信息的更新, 可以同时更新信息，后面的覆盖前面的。
      为了防止数据的覆盖，每个线程一个BaseMode
      权限说明:
      需要从session获取用户名字,做身份和权限的验证
      base_mode 算是thread-local data吧 threading.local, 和werkzeug中local
      的实现，暂时还不知道怎么使用或移至
    """
    # name = request.form["name"] 如果不存在key(name)将导致 400 Bad Request
    print "111111111111111111111111111"
    updateFrm = base.BaseUpdateForm()
    if updateFrm.validate_on_submit():
        base_mode = getMode(BaseMode)
        base_mode.clear()                             # 一直存在的实例.数据需要清理, cache
        base_mode.doc.update(updateFrm.asDict())
        base_mode.updateQuery.update({"name": base_mode.name})
        ret = base_mode.update(upsert=False, safe=True)

        if ret["n"] == 0:
            error = u"不存在的记录"
            # flash(_(u"不存在的记录"), error)
        elif ret["err"]:
            error = str(ret["err"])
        elif ret["updatedExisting"]:            # 这是更新
            error = "update success"
        else:
            error = "insert success"
        print "2222222222222222222222222222"
        flash(_(u"%s"%(error, )), "error")

    return render_template_string("{% import 'form.html' as forms with context %}\
                <div id='flashed'>\
                        <ul>\
                        {% for category, msg in get_flashed_messages(with_categories=true) %}\
                            <li class='alert alert-{{ category }}'> {{ msg }}</li>\
                        {% endfor %}\
                        </ul>\
                </div>\
                 <div class='span4'>{{ forms.myForm(updateForm, updateURL) }}</div>", updateForm=updateFrm, updateURL="base.update"
        )


#========================================================
# # 使用ajax.post(ajax)做下面的请求
#========================================================
@baseView.route("/flymove", methods=["POST", "GET"])
def fly_move():
    """
    @param frmBase: 到那个基地, form 提交
    """
    try:
        flyID = int(request.form["flyID"])   # 飞机的ID
        toBase = request.form["toBase"]
        fromBase = request.form["fromBase"]
        flyDes = request.form["flyDes"]         # 描述，可能是固定的原因
    except:
        raise AppException("参数错误")

    # 可以直接查询db.base.find_one({"id":toBase"}}, 在python里面做分析
    if not db.base.find_one({"id": toBase,
                             "flyList": {"$elemMatch": {"$in": [flyID, ]}}}):
        return "哪里跑"

    if not db.base.find_one({"id": fromBase}):
        return "目标不可大"
    if not db.fly.find_one({"flyID": flyID, "parent": fromBase}):
        return "数据不一致"

    # 数据的移动操作， 这样的操作不是好的操作， 依旧是不安全的
    db.base.update({"id": toBase},
                    {"$pull": {"flyList": {"$elemMatch": {"$in": [flyID, ]}}}})
    db.base.update({"id": fromBase},
                   {"$addToSet": {"flyList": [flyID, flyDes, ]}})

    return "ok"
