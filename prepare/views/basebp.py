#-*-coding:utf-8 -*-
from threading import Lock

from flask import Blueprint
from flask import logging

_logger_lock = Lock()

class BaseAppBP(Blueprint):
    """Blueprint感觉少些东西
    """
    def __init__(self, name, import_name, static_folder=None,
                 static_url_path=None, template_folder=None,
                 url_prefix=None, subdomain=None, url_defaults=None, 
                 debug = False):
        """
        这个debug其实是为了作日志输出使用的，不过有感觉有点多与
        """
        super(BaseAppBP, self).__init__(name, import_name, static_folder,
                                static_url_path, template_folder,
                                url_prefix, subdomain, url_defaults)

        self.debug_log_format = (
                '-' * 80 + '\n' + 
                '%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n' +
                '%(message)s\n' +
                '-' * 80
                )
        self.debug = debug
        self.debug_name = name
        self.__logger = None

    @property
    def logger(self):
        """
        更为详细完整的代请见flask module的app.py文件
        """
        if self.__logger:
            return self.__logger

        if not self.__logger:   # 多线程创建
            _logger_lock.acquire() 
            if not self.__logger:
                self.__logger = logging.create_logger(self)
            _logger_lock.release()
       
        return self.logger

