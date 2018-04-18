# coding:utf-8
# 静态html文件处理
from flask import Blueprint,current_app

# 创建返回静态html文件的蓝图
html_bule = Blueprint("html",__name__)


@html_bule.route("/<file_name>")
def get_static_html(file_name):

    # 提示：如何才能使用file_name找到对应的html文件，路径是什么？
    # /static/html/register.html
    file_name = "html/%s"%file_name

    print file_name

    # 根据file_name拼接的全路径，去项目路径中查找静态html文件，并响应给浏览器
    return current_app.send_static_file(file_name)



