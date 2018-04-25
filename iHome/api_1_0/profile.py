# coding:utf-8
# 个人中心
from iHome import db,constants
from iHome.api_1_0 import api
from flask import session, current_app, jsonify,request,g
from iHome.models import User
from iHome.utils.response_code import RET
from iHome.utils.image_storage import upload_image
from iHome.utils.common import login_required




@api.route("/users/auth",methods=["GET"])
@login_required
def get_user_auth():
    """提供实名认证数据
       0.判断用户是否登录
       1.查询当前登录用户user信息
       2.构造响应的实名认证的数据
       3.响应实名认证的数据
       """
    # 1.查询当前登录用户user信息
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户数据失败')
    if not user:
        return jsonify(errno=RET.NODATA, errmsg='用户不存在')

    # # 2.构造响应的实名认证的数据
    # response_auth_dict = user.auth_to_dict()
    # 3.响应实名认证的数据
    return jsonify(errno=RET.OK, errmsg='OK', data= user.auth_to_dict())

@api.route("/users/auth",methods=["POST"])
@login_required
def set_user_auth():
    """实名认证
        0.判断用户是否登录
        1.获取实名认证参数：real_name,id_card,并判断是否为空
        2.查询当前的登录用户user模型
        3.将real_name,id_card赋值给user模型
        4.保存到数据库
        5.响应实名认证结果
        """
    #  1.获取实名认证参数：real_name,id_card,并判断是否为空
    json_dict = request.json
    real_name = json_dict.get("real_name")
    id_card = json_dict.get("id_card")


    # todo 实际开发中，需要对身份证号码格式校验。一般会使用第三方的平台实名认证
    if not all([real_name,id_card]):
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    # 2.查询当前的登录用户user模型
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)

        return jsonify(errno=RET.DBERR, errmsg='查询用户数据失败')
    if not user:
        return jsonify(errno=RET.PARAMERR, errmsg='用户不存在')
    # 3.将real_name,id_card赋值给user模型
    user.real_name = real_name
    user.id_card = id_card

    # 4.保存到数据库
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存用户实名认证数据失败')

    # 5.响应实名认证结果
    return jsonify(errno=RET.OK, errmsg='保存成功')

@api.route("/users/name",methods=["PUT"])
@login_required
def set_user_name():
    """修改用户名
        0.TODO 判断用户是否登录
        1.获取新的用户名，并判断是否为空
        2.查询当前的登录用户
        3.将新的用户名赋值给当前的登录用户的user模型
        4.将数据保存到数据库
        5.响应修改用户名的结果
       """
    # 2.查询当前的登录用户
    # 下面方式取不到数据会报错，选用get取得数据,返回None
    # user_id = session["user_id"]
    user_id = g.user_id

    # 1.获取新的用户名，并判断是否为空
    try:
        user_name = request.json.get('user_name')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='缺少必传参数')
    # 2.查询当前的登录用户
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
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存用户名失败')

    # 把保存在session里的用户名修改
    session["name"] = user_name

    # 5.响应修改用户名的结果
    return jsonify(errno=RET.OK, errmsg="OK")

@api.route("/users/avatar",methods=["POST"])
@login_required
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
    # 2.查询当前的登录用户
    # 下面方式取不到数据会报错，选用get取得数据
    # user_id = session["user_id"]
    user_id = g.user_id

    # 1. 获取用户上传的头像数据，并校验
    try:
        avatar_data = request.files.get("avatar")
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='获取用户头像失败')


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
@login_required
def get_user_info():
    """提供个人信息
        0.TODO 判断用户是否登录
        1.从session中获取当前登录用户的user_id
        2.查询当前登录用户的user信息
        3.构造个人信息的响应数据
        4.响应个人信息的结果
        """
    # 1.从session中获取当前登录用户的user_id
    # 下面方式取不到数据会报错，选用get取得数据
    # user_id = session["user_id"]

    user_id = g.user_id
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
