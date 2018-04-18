# coding:utf-8
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import redis

from flask_wtf import CSRFProtect
from flask_session import Session
from config import Config
from config import config


# 创建连接数据的对象,在配置后面
db = SQLAlchemy()

def get_app(config_name):
    # todo 使用工厂设计模式，根据传入不同的config_name,找到不同的配置

    app = Flask(__name__)

    # 加载配置参数
    app.config.from_object(config[config_name])

    # 创建连接数据的对象,在配置后面
    #db = SQLAlchemy()
    # 先创建对象在，调用init_app传入app
    db.init_app(app)


    # 创建redis数据库链接对象 :
    # store:仓库
    # strict : 严格的；绝对的；精确的；详细的
    # StrictRedis类里面指定了host和port的缺省默认参数，可以不指定参数
    redis_store = redis.StrictRedis(host=config[config_name], port=config[config_name])

    # 开启csrf保护
    CSRFProtect(app)

    # 使用flask_session将session数据写入redis数据库
    Session(app)

    return app