# coding:utf-8
# 定义公共的工具文件

from werkzeug.routing import BaseConverter
from flask import session,jsonify,g
from iHome.utils.response_code import RET
from functools import wraps


class RegexConverter(BaseConverter):
    """自定义路由转换器，根据外界的正则，匹配指定的字符串"""

    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)

        # 保存正则
        self.regex = args[0]

def login_required(view_func):
    """自定义装饰器判断用户是否登录
    使用装饰器装饰函数时，会修改被装饰的函数的__name属性和被装饰的函数的说明文档
    为了不让装饰器影响被装饰的函数的默认的数据，我们会使用@wraps装饰器，提前对view_funcJ进行装饰
    """

    @wraps(view_func)
    def wraaper(*args, **kwargs):
        """具体实现判断用户是否登录的逻辑"""
        user_id = session.get('user_id')
        if not user_id:
            return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')
        else:
            # 当用户已登录，使用g变量记录用户的user_id，方便被装饰是的视图函数中可以直接使用
            g.user_id = user_id
            # 执行被装饰的视图函数
            return view_func(*args, **kwargs)

    return wraaper
