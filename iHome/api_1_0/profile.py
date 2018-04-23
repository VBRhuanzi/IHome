# coding:utf-8
# 个人中心
from iHome import db,constants
from iHome.api_1_0 import api
from flask import session, current_app, jsonify,request
from iHome.models import User
from iHome.utils.response_code import RET
from iHome.utils.image_storage import upload_image


@api.route("/users/name",methods=["PUT"])
def set_user_name():
    """修改用户名
        0.TODO 判断用户是否登录
        1.获取新的用户名，并判断是否为空
        2.查询当前的登录用户
        3.将新的用户名赋值给当前的登录用户的user模型
        4.将数据保存到数据库
        5.响应修改用户名的结果
       """
    # 1.获取新的用户名，并判断是否为空
    try:
        user_name = request.json.get('user_name')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='缺少必传参数')
    print user_name

    # 2.查询当前的登录用户
    user_id = session["user_id"]
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户数据失败')
    if not user:
        return jsonify(errno=RET.NODATA, errmsg="用户不存在")

    #  3.将新的用户名赋值给当前的登录用户的user模型
    user.name = user_name
    try:
        #  4.将数据保存到数据库
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存用户名失败')

    # 5.响应修改用户名的结果
    return jsonify(errno=RET.OK, errmsg="OK")









@api.route("/users/avatar",methods=["POST"])
def upload_avatar():
    """
    上传用户头像
    0.TODO 判断用户是否登录
    1.获取用户上传的头像数据，并校验
    2.查询当前的登录用户
    3.调用上传工具方法实现用户头像的上传
    4.将用户头像赋值给当前的登录用户的user模型
    5.将数据保存到数据库
    6.响应上传用户头像的结果
    """
    # 1. 获取用户上传的头像数据，并校验
    try:
        avatar_data = request.files.get("avatar")
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='获取用户头像失败')

    # 2.查询当前的登录用户
    user_id = session["user_id"]
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户数据失败')
    if not user:
        return jsonify(errno=RET.NODATA, errmsg="用户不存在")

    # 3.调用上传工具方法实现用户头像的上传
    try:
        key = upload_image(avatar_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='上传用户头像失败')

    # 4.将用户头像赋值给当前的登录用户的user模型
    user.avatar_url = key
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存用户头像失败')

    # 6.响应上传用户头像的结果
    avatar_url = constants.QINIU_DOMIN_PREFIX + key
    return jsonify(errno=RET.OK, errmsg="OK", data=avatar_url)



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
