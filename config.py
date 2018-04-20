# coding:utf-8
import logging
import redis


class Config(object):
    """配置参数"""

    DEBUG = True

    # 秘钥
    SECRET_KEY = 'q7pBNcWPgmF6BqB6b5VICF7z7pI+90o0O4CaJsFGjzRsYiya9SEgUDytXvzFsIaR'

    # 配置mysql数据库：真实开发不写127，写数据库的真实的ip
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/iHome_GZ01'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 配置redis数据库 : 实际开发使用redis数据库的真实ip
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # 配置session参数
    # 指定session存储到redis
    SESSION_TYPE = 'redis'
    # 指定要使用的redis的位置
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 是否使用secret_key签名session_data
    SESSION_USE_SIGNER = True
    # 设置session的过期时间
    PERMANENT_SESSION_LIFETIME = 3600 * 24 # 有效期为一天

class Development(Config):
    """开发模式下配置"""

    # 调试级别
    LOGGING_LEVEL = logging.DEBUG



class Production(Config):
    """生产环境，部署上线之后的配置"""
    DEBUG = True
    # 配置mysql数据库：真实开发不写127，写数据库的真实的ip
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/iHome_GZ01'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 设置session的过期时间
    PERMANENT_SESSION_LIFETIME = 3600 * 24  # 有效期为一天

    LOGGING_LEVEL = logging.WARN



class UnitTest(Config):
    """测试环境"""
    pass


configs = {
    "dev":Development,
    "pro":Production,
    "test":UnitTest
}
