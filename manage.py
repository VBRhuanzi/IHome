# coding:utf-8
# 程序入口 日期：2018.4.17 时间： 开发者： frank

from flask.ext.script import Manager
from flask_migrate import Migrate, MigrateCommand



# from iHome import app,db
from iHome import get_app,db

app = get_app('dev')

# 创建脚本管理器
manager = Manager(app)

# 让迁移时，app和db建立链接,写注意不要搞反了
Migrate(app, db)

# 将数据库迁移的脚本、命令添加到脚本管理器对象
manager.add_command('db', MigrateCommand)


@app.route('/')
def index():
    # redis_store.set("key", "value")
    #
    # session["name"] = 'ketty'

    return "index"


if __name__ == '__main__':
    manager.run()
