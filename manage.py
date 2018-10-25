# -*- coding:utf-8 -*-  
# ====#====#====#====
# @CreateTime  : 2018/10/16 10:29
# @Author      : Jeanfo
# @FileName    : manage.py.py
# @Software    : PyCharm
"""
 @Desc:
"""
import sys
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app
from exts import db
from scripts.zhihu_scrapy import ZhihuScrapy
from models import (
    User,
    Question,
    Answer
)


reload(sys)
sys.setdefaultencoding('utf-8')

manager = Manager(app)

# 使用Migrate绑定app和db
migrate = Migrate(app, db)

# 添加迁移脚本命令到manager中
manager.add_command('db', MigrateCommand)

manager.add_command('zhihu_scrapy', ZhihuScrapy())


if __name__ == "__main__":
    manager.run()
