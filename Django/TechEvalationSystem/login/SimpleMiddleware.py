import re
from django.shortcuts import redirect
from django.urls import reverse


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # print("SimpleMiddleware")
        # One-time configuration and initialization.

    def __call__(self, request):
        path = request.path
        # print("url:", path)
        """
            1.判断是否登录
            2.判断是否访问pingjia开头
        """
        # 允许后台不登录情况下访问的路径
        urllist = ['/', '/logout/', '/login/']
        if re.match(r'^/students/', path) and (path not in urllist):
            # 重定向到登录页
            if 'xuehao' not in request.session:
                return redirect(reverse("login"))
        if re.match(r'^/teachers/', path) and (path not in urllist):
            # 重定向到登录页
            if 'teacher_id' not in request.session:
                return redirect(reverse("login"))
        if re.match(r'^/myadmin/', path) and (path not in urllist):
            # 重定向到登录页
            if 'name' not in request.session:
                return redirect(reverse("login"))

        response = self.get_response(request)
        return response
