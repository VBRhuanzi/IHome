# coding:utf-8
# 图片验证和短信验证
import logging
import re,random

from iHome import constants
from iHome import redis_store
from iHome.utils.sms import CCP
from . import api
from flask import make_response, request, abort, jsonify, current_app, json

# 调用方法生成图片验证
from iHome.utils.captcha.captcha import captcha
from iHome.utils.response_code import RET


@api.route("/sms_code", methods=["POST"])
def send_sms_code():
    """发送短信验证码
    1.获取参数:手机号，验证码，uuid
    2.判断是否缺少参数，并对手机号格式进行校验
    3.获取服务器存储的验证码
    4.跟客户端传入的验证码进行对比
    5.如果对比成功就生成短信验证码
    6.调用单例类发送短信
    7.如果发送短信成功，就保存短信验证码到redis数据库
    8.响应发送短信的结果
    """
    # 获取参数:手机号，验证码，uuid
    josn_str = request.data
    josn_dict = json.loads(josn_str)

    print ">"*50,josn_dict

    mobile = josn_dict.get("mobile")
    imageCode_client = josn_dict.get("imageCode")
    uuid = josn_dict.get("uuid")

    # 判断是否缺少参数，并对手机号格式进行校验
    if not all([mobile, imageCode_client, uuid]):
        return jsonify(errno=RET.PARAMERR, errmsg="缺少参数")
    if not re.match(r"^1([358][0-9]|4[579]|66|7[0135678]|9[89])[0-9]{8}$", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式错误")

    # 获取服务器存储的验证码
    try:
        imageCode_server = redis_store.get('ImageCode:%s' % last_uuid)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询验证码错误")
    # 判断取得的数据是否为空
    if not imageCode_server:
        return jsonify(errno=RET.DBERR, errmsg="查询验证码不存在")

    # 跟客户端传入的验证码进行对比
    if imageCode_client.lower() != imageCode_server.lower():
        return jsonify(errno=RET.DBERR, errmsg="验证码输入有误")

    #如果对比成功就生成短信验证码
    # "%06d"-不够六位补零
    sms_code = "%06d" % random.randint(0,999999)

    result = CCP().send_sms_code(mobile,[sms_code,5],1)
    print ">"*80

    if result != 1:
        return jsonify(errno=RET.THIRDERR,errmsg="发送短信验证码失败")

    try:
        redis_store.set("SMS:%s" % mobile,sms_code,constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='存储短信验证码失败')

        # 8.响应发送短信的结果
    return jsonify(errno=RET.OK, errmsg='发送短信验证码成功')



last_uuid = ''


@api.route("/image_code", methods=["GET"])
def get_image_code():
    """提供图片验证码
       1.获取uuid，并校验uuid
       2.生成图片验证码
       3.使用redis数据库缓存图片验证码，uuid作为key
       4.响应图片验证码
       """
    # 1.获取uuid，并校验uuid
    uuid = request.args.get('uuid')
    if not uuid:
        abort(403)

    # 2.生成图片验证码
    name, text, image = captcha.generate_captcha()
    # print text
    # logging.debug('验证码内容为：' + text)
    current_app.logger.debug('app验证码内容为：' + text)

    try:
        # 3.使用redis数据库缓存图片验证码，uuid作为key

        # 如果有last_uuid
        if last_uuid:
            redis_store.delete('ImageCode:%s' % last_uuid)

        # 过期时间300秒
        redis_store.set('ImageCode:%s' % uuid, text, constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        print ">>>>>>>>>>>>>>>", e
        logging.error(e)
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存验证码失败')

    # 记录当前的uuid,方便下次使用时作为上一次的uuid，删除上次的text

    global last_uuid
    last_uuid = uuid

    # 4.响应图片验证码
    # 修改响应头信息，指定响应的内容是image/jpg
    response = make_response(image)
    response.headers['Content-Type'] = 'image/jpg'
    # 响应图片验证码
    return response
