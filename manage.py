# coding:utf-8
# 程序入口 日期：2018.4.17 时间： 开发者： frank
from flask import Flask
from flask.ext.script import Manager
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis


class Config(object):
    """配置参数：重写系统默认的配置参数"""
    DEBUG = True
    # 配置mysql数据库 ， 真实开发不写127 ， 写数据库的真实ip
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/vbr_iHome"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379


app = Flask(__name__)

# 加载配置参数
app.config.from_object(Config)

# 创建连接数据的对象,在配置后面
db = SQLAlchemy(app)

# 创建redis数据库链接对象 :
# store:仓库
# strict : 严格的；绝对的；精确的；详细的
# todo StrictRedis类里面指定了host和port的缺省默认参数，可以不指定参数
redis_store = StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)

# 创建脚本管理器
manager = Manager(app)


@app.route('/')
def index():
    redis_store.set("key","value")
    return "index"



if __name__ == '__main__':
    manager.run()
