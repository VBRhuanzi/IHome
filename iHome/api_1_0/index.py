# coding:utf-8


from . import api

from iHome import redis_store


@api.route('/')
def index():
    redis_store.set("key", "value")
    #
    # session["name"] = 'ketty'

    return "index"
