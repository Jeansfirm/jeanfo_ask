# -*- coding:utf-8 -*-  
# ====#====#====#====
# @CreateTime  : 2018/10/17 9:31
# @Author      : Jeanfo
# @FileName    : decorators.py
# @Software    : PyCharm
"""
 @Desc:
"""
from functools import wraps
from flask import (
    session,
    redirect,
    url_for
)


# 登录限制装饰器
def login_required(func):
    @wraps(func)  # 保持被装饰函数的函数名__name__
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper