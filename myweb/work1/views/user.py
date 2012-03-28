#-*- coding:utf-8 -*-
"""
登录的处理, session 储存到数据库, copy cookie认倒霉吧
"""
import md5
from bson import binary

from flask import jsonify
from flask import Blueprint
from flask import url_for, redirect, render_template, request, session

from common import getDB

from forms import LoginForm
db = getDB("app")
userView = Blueprint("user", __name__, url_prefix="/user", 
                    static_folder="static"    
            )


@userView.route("/", methods=["GET", "POST"])
def get():
    """返回登录界面
    """
    if session.get("name"):
       return redirect(url_for("base.get_all"))
    form = LoginForm(login=request.args.get("username", None),
                     next=request.args.get("next", None))
    
    if form.validate_on_submit():
        userInfo = db.user.find_one({"name": form.username.data,
                                 "password": binary.Binary(md5.md5(form.password.data).digest())},
                                {"_id": 0})

        if userInfo is None:
            return jsonify(message="用户名字或密码错误")  # 应该返回错误编码不是直接的文字
        if userInfo.get("power", None) == None:
            return jsonify(message="你的没有权限")

        session["logined"] = True
        session["name"] =  userInfo["name"]
        print userInfo     
        # g.power = userInfo["power"]
        return jsonify(message="ok")

    return render_template("login.html", form = form)


@userView.route("/logout", methods=["GET",])
def logout():
    if "name" in session:
        session.pop("name")
    return redirect(url_for("index"))

@userView.route("/", methods=["POST", ])
def login_post():
    """简单的验证用户
    注意:password全部明文
    密码储存:[salt]+password, 现在没有salt, password储存方式：二进制, 十六进制字符刱
    """
    print "111111111111111!!!!"
    username = request.form.get("username")
    password = request.form.get("password")  # 明文从客户端传送
    # power:权限
    userInfo = db.user.find_one({"name": username,
                                 "password": binary.Binary(md5.md5(password).digest())},
                                {"_id": 0})
    if userInfo is None:
        return jsonify(message="用户名字或密码错误")  # 应该返回错误编码不是直接的文字
    if userInfo.get("power", None) == None:
        return jsonify(message="你的没有权限")

    session["logined"] = True
    session["name"] =  userInfo["name"]
    print userInfo     
    # g.power = userInfo["power"]
    return jsonify(message="ok")


