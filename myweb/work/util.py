#-*- coding:utf-8 -*-
"""
工具模块
"""
import threading
import weakref
from threading import Lock
from functools import update_wrapper
from flask import session, render_template, g, flash
from common import getDB
from mode import Mode
from flask import redirect, url_for


_g_lock = Lock()
db = getDB("app")
_twRef = {}
_localModes = {}


def synchronize(method):
    """
    怒了啊，提供线程同步的装饰器
    """
    def Angry(*args, **kwargs):
        with _g_lock:
            return method(*args, **kwargs)

    return update_wrapper(Angry, method)


def app_verifyUser(method):
    """
    凑合着用吧。验证用户session
    现在用户的ID， 同时也为Session ID
    """
    def default(*args, **kwargs):
        print "-----------------------"
        name = session.get("name")
        if name is None:
            return redirect(url_for("user.get"))
            # return render_template("login.html")

        userInfo = db.user.find_one({"name": name})
        if not userInfo:
            return redirect(url_for("user.get"))
            # return render_template("login.html")

        name, pwd = userInfo["name"], userInfo["password"]
        #if session_key != md5.md5(name + pwd).digest():
        #    return render_template("login.html")
        g.user = name
        flash(u"欢迎回来")
        g.logined = True
        return method(*args, **kwargs)     # 可以提前返回
        # return render_template("index.html")
    return update_wrapper(default, method)


def release_mode(threadRef, name, tid):
    """
    线程是否后，ident 将被回收利用
    """
    global __twRef
    if tid in _twRef:
        _twRef.pop(tid)
    if name in _localModes and tid in _localModes[name]:
        _localModes[name].pop(tid)


def getMode(cls, name=None):
    assert issubclass(cls, Mode), u"基类不是Mode"

    t = threading.current_thread()
    tid = t.ident
    if name is None:
        name = cls.__name__

    if tid not in _twRef:   # 一个线程可能多次被调用, 不重复添加
        _twRef[tid] = weakref.ref(t, lambda r, i=tid, name=name: release_mode(r, name, tid))  # 2
    modes = _localModes.setdefault(name, {})  # 1

    return modes.setdefault(tid, cls())
