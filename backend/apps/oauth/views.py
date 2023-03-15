import re
from django.shortcuts import render, redirect
from AgentLogin import AgentLogin
from django.urls import reverse
from django.views import View
from django.conf import settings  # 这个属性是动态获取项目配置模块
from django.http import *
from django_redis import get_redis_connection
from .models import *
from django.contrib.auth import login
from .utils import generate_secret_openid, check_secret_openid
from apps.userapp.models import Users


class QQLoginView(View):

    def get(self, request):
        # 注意配置虚拟主机回调地址 127.0.0.1    回调地址 再windows下的hosts配置文件中找
        # 并把回调地址添加到配置文件中    并把项目启动端口号改成QQ那个对应的
        # 且重新定义一个视图让他回调到我们的视图中
        # 我现在申请不了QQ互联所以没法用

        qq_url = AgentLogin.qq_url(settings.QQ_CLIENT_ID,
                                   settings.QQ_REDIRECT_URI)
        return JsonResponse({'code': 200, 'errormsg': 'OK', 'login_url': qq_url})


class QQAuthUserView(View):

    def get(self, request):
        # 获取code参数 这个code就是QQ服务器那边得到的
        code = request.GET.get('code', '')

        # 校验参数
        if not code:
            return HttpResponseForbidden('缺少参数')
        nickname, openid = AgentLogin.qq(settings.settings.QQ_CLIENT_ID,
                                         settings.QQ_APP_KEY,
                                         settings.QQ_REDIRECT_URI,
                                         code
                                         )
        # 通过openid来判断当前用户是否绑定项目用户
        try:
            qq_user = QQAuthUser.objects.get(openid=openid)
        except QQAuthUser.DoesNotExist:
            # 未绑定用户
            # 加密openid数据
            sec_openid = generate_secret_openid(openid)
            # 传递加密数据给用户绑定页面
            return render(request, 'oauth/oauth_user.html', {'sec_openid': sec_openid})
        else:
            # 已绑用户
            user = qq_user.user
            # 状态保持
            login(request, user)
            return redirect(reverse('newsapp:index'))

    def post(self, request):
        # 将当前qq用户绑定为项目用户
        # 接收参数
        sec_openid = request.POST.get('sec_openid', '')
        phone = request.POST.get('phone', '')
        sms_code_client = request.POST.get('msgcode', '')
        password = request.POST.get('password', '')

        # 校验参数
        if not all([phone, password, sms_code_client, sec_openid]):
            return HttpResponseForbidden('缺少必传参数')
        # 判断⼿机号是否合法
        if not re.match(r'^1[35789]\d{9}$', phone):
            return HttpResponseForbidden('请输⼊正确的⼿机号码')
        # 判断密码是否合格
        if not re.match(r'^[0-9A-Za-z]{3,8}$', password):
            return HttpResponseForbidden('请输⼊3,8位的密码')
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s' % phone)
        if sms_code_server is None:
            return render(request, 'oauth/oauth_user.html',
                          {'sms_code_errmsg': '⽆效的短信验证码'})
        if sms_code_client != sms_code_server.decode():
            return render(request, 'oauth/oauth_user.html',
                          {'sms_code_errmsg': '输⼊短信验证码有误'})
        # 判断openid是否有效：错误提示放在sms_code_errmsg位置
        openid = check_secret_openid(sec_openid)
        if not openid:
            return render(request, 'oauth/oauth_user.html',
                          {'openid_errmsg': '⽆效的openid'})

        # 获取项目用户
        try:
            user = Users.objects.get(phone=phone)
        except Users.DoesNotExist:
            user = Users.objects.create_user(username=phone, password=password, phone=phone)
        else:
            # 判断密码是否正确
            if not user.check_password(password):
                return render(request, 'oauth/oauth_user.html', {'qq_login_error': '密码错误'})

        # 绑定用户
        try:
            QQAuthUser.objects.create(user=user, openid=openid)
        except Exception as e:
            return render(request, 'oauth/oauth_user.html', {'reg_error_msg': '用户绑定失败'})

        # 状态保持
        login(request, user)

        # 响应结果
        return redirect(reverse('newsapp:index'))


