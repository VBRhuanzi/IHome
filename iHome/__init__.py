# coding:utf-8
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import redis

from flask_wtf import CSRFProtect
from flask_session import Session
from config import Config
from config import configs
from utils.common import RegexConverter

# 创建连接数据的对象,在配置后面
db = SQLAlchemy()

# 把redis数据库链接对象定义为全区
redis_store = None

def setUpLogging(level):
    """根据开发环境设置入职等级"""

    # 设置日志的记录等级
    logging.basicConfig(level=level)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
    # 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


def get_app(config_name):
    # todo 使用工厂设计模式，根据传入不同的config_name,找到不同的配置

    setUpLogging(configs[config_name].LOGGING_LEVEL)

    app = Flask(__name__)

    # 加载配置参数
    app.config.from_object(configs[config_name])

    # 创建连接数据的对象,在配置后面
    #db = SQLAlchemy()

    # 先创建对象在，调用init_app传入app
    db.init_app(app)


    # 创建redis数据库链接对象 :
    # store:仓库
    # strict : 严格的；绝对的；精确的；详细的
    # StrictRedis类里面指定了host和port的缺省默认参数，可以不指定参数
    global redis_store
    redis_store = redis.StrictRedis(host=configs[config_name].REDIS_HOST,
                                    port=configs[config_name].REDIS_PORT)
    # 开启csrf保护
    CSRFProtect(app)

    # 使用flask_session将session数据写入redis数据库
    Session(app)

    # 将自定义的路由转换器添加到路由转换器列表
    app.url_map.converters["re"] = RegexConverter


    # 注册api蓝图
    # 哪里注册蓝图就在哪里使用蓝图，避免某些变量在导入时还不存在，但是已经被导入
    from iHome.api_1_0 import api
    app.register_blueprint(api)

    # 注册处理静态文件html蓝图
    from iHome.web_html import html_bule
    app.register_blueprint(html_bule)

    #


    return app