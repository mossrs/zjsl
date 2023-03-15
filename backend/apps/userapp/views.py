import json
from django.contrib.auth import *
from django.db import DatabaseError
from django.shortcuts import *
from django.views.generic.base import View
from django.http import *
from utils.exceptions import *
from apps.userapp.models import *


class LoginView(View):

    def get(self, request):
        # 显示登录首页
        next = request.GET.get('next', '')
        return render(request, 'userapp/login.html', {'next': next})

    def post(self, request):
        # 1 接收请求
        next = request.POST.get('next', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        remember = request.POST.get('remember', '')

        # 2 校验参数
        if not all([username, password, remember]):
            return HttpResponseForbidden('缺少必传参数')

        # 3 认证参数是否正确
        user = authenticate(username=username, password=password)
        if not user:
            return render(request, 'userapp/login.html', {'login_error': '用户名或密码错误'})

        # 4 状态保持
        login(request, user)
        # 这个前端因为设置了复选框 默认是on 不选就不是on
        if remember != 'on':
            # 关闭浏览器失效
            request.session.set_expiry(0)
        else:
            # 默认14天有效期
            request.session.set_expiry(None)
        if next:
            return redirect(next)
        # 5 响应结果
        return redirect(reverse('newsapp:index'))


class UserCenterView(View):

    # 显示用户中心页面
    def get(self, request):
        # 判断注册用户是否已登录 使用该属性 如果登录则true 否则false
        # 但如果登录的地方太多则需要写很多重复代码 因此引入login_required装饰器 就不用写下面代码了
        # if request.user.is_authenticated:
        #     return render(request, 'userapp/user_center.html')
        # else:
        #     return redirect(reverse('newsapp:index'))
        return render(request, 'userapp/user_center.html')


class EmailsView(View):

    # 保存用户邮箱地址
    def post(self, request):
        # 获取表单内容 {'email': '', 'userid': ''}
        params = request.body.decode()
        if not params:
            return JsonResponse({'code': '4001', 'errormsg': '缺少必传参数'})

        dict_params = json.loads(params)
        count = Users.objects.filter(id=dict_params['userid']).update(email=dict_params['email'])
        if count > 0:
            return JsonResponse({'code': 200, 'errormsg': 'OK'})
        return JsonResponse({'code': '500', 'errormsg': '保存失败'})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('newsapp:index'))


class RegisterView(View):

    def get(self, request):
        return render(request, 'userapp/register.html')

    def post(self, request):
        # 1 接收请求参数
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        phone = request.POST.get('phone', '')

        # 2 校验参数
        if not all([username, phone, password]):
            raise Forbidden('缺少必要参数')
        elif not re.match(r'^\w{5,8}$', username):
            raise Forbidden('请重新输入用户名')
        elif not re.match(r'^\w{5,8}$', password):
            raise Forbidden('请重新输入密码')
        elif not re.match(r'^1[3578]\d{9}$', phone):
            raise Forbidden('请重新输入手机号')

        # 3 保存数据到数据库
        try:
            # 这里面django的有关于数据库的一些错误
            user = Users.objects.create_user(username=username, password=password, phone=phone)
        except DatabaseError:
            return render(request, 'userapp/register.html', {'reg_error_code': '注册失败'})

        # 4 状态保持功能
        login(request, user)

        # 5 返回响应
        return redirect(reverse('newsapp:index'))


class UsernameCountView(View):

    def get(self, request, username):
        count = Users.objects.filter(username=username).count()
        return JsonResponse({'code': 200, 'errormsg': 'OK', 'count': count})


class PhoneCountView(View):

    def get(self, request, phone):
        count = Users.objects.filter(phone=phone).count()
        return JsonResponse({'code': 200, 'errormsg': 'OK', 'count': count})




