# coding:utf-8
# 个人中心

from iHome.api_1_0 import api
from flask import session, current_app, jsonify
from iHome.models import User
from iHome.utils.response_code import RET


@api.route("/users/auth", methods=["GET"])
def my():
    """提供实名认证数据
   0.判断用户是否登录
   1.查询当前登录用户user信息
   2.构造响应的实名认证的数据
   3.响应实名认证的数据
   """
    # 取得用户id

    user_id = session["user_id"]  # 2.查询当前登录用户user信息
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户数据失败')
    if not user:
        return jsonify(errno=RET.NODATA, errmsg="用户不存在")

    # 2.构造响应的实名认证的数据
    resqonse_info_dict = {
        'user_id': user.id,
        'avatar_url': user.avatar_url,
        'name': user.name,
        'mobile': user.mobile
    }

    # 3.响应实名认证的数据
    return jsonify(errno=RET.OK, errmsg="OK", data=resqonse_info_dict)
