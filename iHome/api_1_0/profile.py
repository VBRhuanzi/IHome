# coding:utf-8
# 个人中心

from iHome.api_1_0 import api
from flask import session, current_app, jsonify
from iHome.models import User
from iHome.utils.response_code import RET

@api.route("/api/v1.0/user/avatar",methods=["POST"])
def set_user_avatar():
    """ """
    pass




@api.route("/users", methods=["GET"])
def get_user_info():
    """提供个人信息
        0.TODO 判断用户是否登录
        1.从session中获取当前登录用户的user_id
        2.查询当前登录用户的user信息
        3.构造个人信息的响应数据
        4.响应个人信息的结果
        """
    # 1.从session中获取当前登录用户的user_id
    user_id = session["user_id"]

    # 2.查询当前登录用户的user信息
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户数据失败')
    if not user:
        return jsonify(errno=RET.NODATA, errmsg="用户不存在")

    # 3.构造响应的实名认证的数据
    # response_info_dict = {
    #     'user_id': user.id,
    #     'avatar_url': user.avatar_url,
    #     'name': user.name,
    #     'mobile': user.mobile
    # }
    #
    # 4.响应实名认证的数据,
    #  使用封装的to_dict方法直接返回当前登陆用户的信息
    # response= user.to_dict()
    # print ">"*20,response
    #
    # return jsonify(errno=RET.OK, errmsg="OK", data=response)

    # # 4.响应实名认证的数据,
    # #  使用封装的to_dict方法直接返回当前登陆用户的信息
    return jsonify(errno=RET.OK, errmsg="OK", data=user.to_dict())
