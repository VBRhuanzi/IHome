# -*- coding:utf-8 -*-
# 登录注册


from . import api
from flask import request, jsonify, current_app
import json, re
from iHome.utils.response_code import RET
from iHome import redis_store,db
from iHome.models import User


@api.route('/users', methods=['POST'])
def register():
    """注册
    1.获取注册参数：手机号，短信验证码，密码
    2.判断参数是否缺少
    3.获取服务器存储的短信验证码
    4.与客户端传入的短信验证码对比
    5.如果对比成功，就创建用户模型User对象，并给属性赋值
    6.将模型属性写入到数据库
    7.响应注册结果
    """

    # 1.获取注册参数：手机号，短信验证码，密码
    # json_str = request.data
    # json_dict = json.loads(json_str)
    # 当我们后端确定前端发来的是json字符串时
    # json_dict = request.get_json()
    json_dict = request.json
    mobile = json_dict.get('mobile')
    sms_code_client = json_dict.get('sms_code')
    password = json_dict.get('password')

    # 2.判断参数是否缺少
    if not all([mobile, sms_code_client, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')
    if not re.match(r'^1([358][0-9]|4[579]|66|7[0135678]|9[89])[0-9]{8}$', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号格式错误')

    # 3.获取服务器存储的短信验证码
    try:
        sms_code_server = redis_store.get('SMS:%s' % mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询短信验证码失败')
    if not sms_code_server:
        return jsonify(errno=RET.NODATA, errmsg='短信验证码不存在')

    # 4.与客户端传入的短信验证码对比
    if sms_code_client != sms_code_server:
        return jsonify(errno=RET.PARAMERR, errmsg='短信验证码输入有误')

    # 5.如果对比成功，就创建用户模型User对象，并给属性赋值
    user = User()
    user.mobile = mobile
    user.name = mobile # 默认把手机号作为用户名，如果不喜欢，后面会提供修改用户名的接口
    # 需要将密码加密后保存到数据库:调用password属性的setter方法
    user.password_hash = password

    # 6.将模型属性写入到数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存用户注册数据失败')

    # 7.响应注册结果
    return jsonify(errno=RET.OK, errmsg='注册成功')
