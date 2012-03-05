#-*- coding:utf-8 -*-
"""
"""
import json

from flask import request#, session
from flask import render_template_string
from basebp import BaseAppBP 
from db import DB as ReaderDB

class PrepareBP(BaseAppBP):
    """
    与app的日志是分开的
    """
    __name = "prepare"
    __url_prefix = "/reader"
    logger_name = "Reader"

    def __init__(self):
        """        
        """
        super(PrepareBP, self).__init__(PrepareBP.__name, __name__, url_prefix = PrepareBP.__url_prefix, debug = True)

    ##########################################
    #  可能module里面有对应的函数
    ##########################################
    @property
    def self_name(self):
        return self.__name

    @property
    def self_urlPrefix(self):
        return self.__url_prefix
 
PrepareView = PrepareBP()

@PrepareView.route("/")
def index():
    return render_template_string("<a href= {{ url_for('.prepare_get', product_name='123') }}> 123 </a>")

@PrepareView.route("/prepare/<product_name>", methods=["get", ])
def prepare_get(product_name):
    """
    不区分大小写,
    """
    # temp = request.args.copy()   # 为了不区分大小写 
    
    client_info = {} 
    client_info["device_id"]        = request.args.get("device_id", "")
    client_info["id"]               = request.args.get("device_model", "")
    client_info["width"]            = request.args.get("width", 0)
    client_info["height"]           = request.args.get("height", 0)
    client_info["clientOS"]         = request.args.get("os", "")
    client_info["clientOS_version"] = request.args.get("osversion", 0)
    client_info["size_model"]       = request.args.get("sizemodel", "")
   
    
    # 线程安全读写操作,如果不存在插入数据库, 然后进行查询
    # 次在这自己验证自己的情况
    ReaderDB.devlist.update({"id":{"$ne":client_info["device_id"]}}, client_info, upsert=True)
    ReaderDB.devmodel.update({"id":{"$ne":client_info["id"]}}, client_info, upsert=True) 
    ReaderDB.sizemodel.update({"id":{"$ne":client_info["size_model"]}}, {"id":client_info["size_model"], "width":client_info["width"], "height":client_info["height"]}, upsert=True)
    
    res = ReaderDB.sizemodel.find_one({"id":client_info["size_model"]})
    if res["width"]  == client_info["width"] and res["height"] == client_info["height"]:
        PrepareView.logger.info("pass", extra = client_info) 
    else:
        PrepareView.logger.error("not match", extra = client_info)
 
    return json.dumps(request.args) 

