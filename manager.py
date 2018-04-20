# coding:utf-8
# 程序入口 日期：2018.4.17 时间： 开发者： frank

from flask.ext.script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import current_app
# from iHome import app,db
from iHome import get_app,db
from iHome import models
 # 没有实际意义，只在迁移前告知迁移脚本，有哪些模型类

app = get_app('dev')

# 创建脚本管理器
manager = Manager(app)

# 让迁移时，app和db建立链接,写注意不要搞反了
Migrate(app, db)

# 将数据库迁移的脚本、命令添加到脚本管理器对象
manager.add_command('db', MigrateCommand)




if __name__ == '__main__':

    print app.url_map

    manager.run()
    # current_app.run()
