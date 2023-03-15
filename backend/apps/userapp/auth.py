import re
from django.contrib.auth.backends import *
from .models import Users


class MultiAccountLoginAuth(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):

        # 管理员用户登陆验证
        # 我们设置了权限功能 当普通用户登陆后 没有数据展示
        # if request is None:
        #     try:
        #         user = Users.objects.get(username=username, is_staff=True)
        #     except:
        #         return None
        #     if user.check_password(password):
        #         return user
        # else:
        # 普通用户登陆验证
        try:
            # 增加用户名或手机号登录功能
            if re.match('^1[135789]\d{9}', username):
                user = Users.objects.get(phone=username)
            else:
                user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            user = None
        if user and user.check_password(password):
            return user
