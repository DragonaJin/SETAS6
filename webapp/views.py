import json
from django.shortcuts import render


def index(request, template_name):

    # 登陆操作
    # 访问数据库
    # 返回用户名username

    return render(request, template_name)


def goto(request, template_name):
    return render(request, template_name)
