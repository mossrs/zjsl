import json
from django import http
from django.conf import settings
from django.db import DataError
from django.shortcuts import render
from django.views.generic.base import View
from .models import *
from django.utils import timezone
from alipay import AliPay
from alipay.utils import AliPayConfig
from utils.views import LoginRequiredJSONMixin
from django.http import JsonResponse


class PaymentView(LoginRequiredJSONMixin, View):

    def post(self, request):
        """
            获取支付宝支付扫码连接
            切忌 那个判断用户是否登陆 你自己写的模块一定要放到第一个继承

        """
        # 接受参数 根据前端来判断格式
        params_json_str = request.body.decode()
        # 校验参数
        if not params_json_str:
            return JsonResponse({'code': 4001, 'errormsg': '缺少必传参数'})
        params_dict = json.loads(params_json_str)
        article_id = params_dict['article_id']
        pay_method = params_dict['pay_method']
        pay_amount = params_dict['pay_amount']

        # 生成流水号
        user = request.user
        order_id = timezone.localtime().strftime("%Y%m%d%H%M%S") + ('%03d' % user.id)
        try:
            order = OrderInfo.objects.create(order_id=order_id, user=user,
                                             pay_method=pay_method, total_amount=pay_amount,
                                             article_id=article_id)
        except DataError:
            return JsonResponse({'code': '4002', 'errormsg': '生成订单失败'})
        app_private_key_string = open('apps/payment/keys/app_private_key.pem').read()
        alipay_public_key_string = open('apps/payment/keys/app_public_key.pem').read()
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调 url
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",                   # RSA 或者 RSA2
            debug=settings.ALIPAY_DEBUG,        # 默认 False
            config=AliPayConfig(timeout=15)     # 可选，请求超时时间
        )
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(order.total_amount),
            subject='诗路浙江%s' % order_id,
            return_url=settings.ALIPAY_RETURN_URL,
            notify_url=settings.ALIPAY_RETURN_URL,
        )
        # 响应结果
        alipay_url = settings.ALIPAY_URL + '?' + order_string
        return JsonResponse({'code': 200, 'errormsg': 'OK', 'alipay_url': alipay_url})


class PaymentStatusView(LoginRequiredJSONMixin, View):

    def get(self, request):
        """
            查询并保存订单结果
        """

        params = request.GET.dict()
        # 这个是获取sign后并剔除 然后使用后面的验证
        signature = params.pop('sign')
        app_private_key_string = open('apps/payment/keys/app_private_key.pem').read()
        alipay_public_key_string = open('apps/payment/keys/app_public_key.pem').read()
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调 url
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=settings.ALIPAY_DEBUG,  # 默认 False
            config=AliPayConfig(timeout=15)  # 可选，请求超时时间
        )
        flag = alipay.verify(params, signature)
        if flag:
            order_id = params.get('out_trade_no')
            trade_no = params.get('trade_no')
            try:
                Payment.objects.create(order_id=order_id, trade_id=trade_no)
            except DataError:
                return http.HttpResponseForbidden('保存支付结果失败')

            OrderInfo.objects.filter(order_id=order_id, status=1).update(status=2)
            return render(request, 'payment/pay_success.html', {'trade_no': trade_no})
        return http.HttpResponseForbidden('非正常请求')
