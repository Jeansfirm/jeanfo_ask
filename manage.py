# -*- coding:utf-8 -*-  
# ====#====#====#====
# @CreateTime  : 2018/10/16 10:29
# @Author      : Jeanfo
# @FileName    : manage.py.py
# @Software    : PyCharm
"""
 @Desc:
"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app
from exts import db
from models import (
    User,
    Question,
    Answer
)

manager = Manager(app)

# 使用Migrate绑定app和db
migrate = Migrate(app, db)

# 添加迁移脚本命令到manager中
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
