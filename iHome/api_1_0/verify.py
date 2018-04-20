# coding:utf-8
# 图片验证和短信验证
import logging
import re

from iHome import constants
from iHome import redis_store
from . import api
from flask import make_response, request, abort, jsonify, current_app, json

# 调用方法生成图片验证
from iHome.utils.captcha.captcha import captcha
from iHome.utils.response_code import RET

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
