# coding:utf-8
# 使用蓝图按照接口版本划分模块

from flask import Blueprint

# 创建1.0版本的蓝图
api = Blueprint("api_1_0",__name__,url_prefix="/api/1.0")


from . import index