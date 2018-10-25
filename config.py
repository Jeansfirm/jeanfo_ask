# -*- coding:utf-8 -*-  
# ====#====#====#====
# @CreateTime  : 2018/10/16 10:23
# @Author      : Jeanfo
# @FileName    : config.py
# @Software    : PyCharm
"""
 @Desc:
"""
import os


# Page config
INIT_PAGE_NUM = 1
INIT_PAGE_LEN = 10

# Debug Mode
DEBUG = True


# DATABASE
DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = '123456'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'jeanfo_ask'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
    DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
)
SQLALCHEMY_TRACK_MODIFICATIONS = False


# SESSION
SECRET_KEY = os.urandom(24)
