import django_redis
from django.http import HttpResponse
from django.shortcuts import render
from django.views import *
from captcha.image import *
from django_redis import *
from django.http import *
from utils.huyi_sms.sms3 import *
import string
import random
import logging

logger = logging.getLogger('django')


class ImgCodeView(View):

    def get(self, request, uuid):
        # 安装 pillow captcha 第三方库
        # 随机生成验证码（4位）
        # 这个属性是得到'0123456789'
        seed = string.digits
        # 这个方法是传入一个集群序列 k=次数 返回每次从集群中随机得到一个对象的k次组成的列表
        r = random.choices(seed, k=4)
        imgcodestr = ''.join(r)

        # 根据验证码数字创建图片验证码 看源码
        imgcode = ImageCaptcha().generate(chars=imgcodestr)

        # 将验证码存入redis
        redis_coon = get_redis_connection(alias='verify_code')
        redis_coon.setex(name='img_%s' % uuid, time=60 * 5, value=imgcodestr)
        # 返回资源给前端
        return HttpResponse(imgcode, content_type='image/png')


class SmsCodeView(View):

    def get(self, request, phone):
        # 1 获取请求参数
        imgcode_client = request.GET.get('imgcode', '')
        uuid = request.GET.get('uuid', '')

        # 2 校验参数
        if not all([phone, imgcode_client, uuid]):
            return JsonResponse({'code': '4001', 'errormsg': '缺少必传参数'})

        # 建立redis连接
        redis_coon = django_redis.get_redis_connection('verify_code')
        is_send = redis_coon.get('is_send_%s' % phone)
        if is_send:
            return JsonResponse({'code': '4004', 'errormsg': '短信发送过于频繁'})
        # 3 获取服务器生成的图片验证码
        imgcode_server = redis_coon.get('img_%s' % uuid)

        # 4 匹配
        if not imgcode_server:
            return JsonResponse({'code': '4002', 'errormsg': '图片验证码失效'})
        if imgcode_client.lower() != imgcode_server.decode('utf8').lower():
            return JsonResponse({'code': '4003', 'errormsg': '图片验证码不一致'})

        # 5 删除验证码 避免客户恶意测试
        try:
            redis_coon.delete('img_%s' % uuid)
        except Exception as e:
            logger.error(e)

        # 6 生成短信验证码 6位
        seed = string.digits
        r = random.choices(seed, k=6)
        smscode_str = ''.join(r)

        # 7 存入redis
        # redis_coon.setex(name='sms_%s' % phone, time=60, value=smscode_str)
        # redis_coon.setex(name='is_send_%s' % phone, time=60, value=1)

        # 使用pipeline 来操作redis
        # 获取管道对象
        pl = redis_coon.pipeline()
        pl.setex('sms_%s' % phone, 60, smscode_str)
        pl.setex('is_send_%s' % phone, 60, 1)
        pl.execute()

        # 8 发送短信验证码
        result = send_sms_code(smscode_str, phone)

        # 9 根据外部接口返回值响应前端结果
        if result['code'] == 2:
            return JsonResponse({'code': 200, 'errormsg': 'OK'})
        return JsonResponse({'code': '5001', 'errormsg': '发送失败'})

        # 异步执行短信验证码功能
        # 启动 celery -A celery_tasks.main worker -l info -P eventlet
        # 必须要在celery_tasks所在的目录下启动
        # from celery_tasks.sms.tasks import huyi_send_sms_code
        # 如果成功执行 返回一个异步任务id类似uuid
        # ret = huyi_send_sms_code.delay(phone, smscode_str)
        # if ret:
        #     return JsonResponse({'code': 200, 'errormsg': 'OK'})
        # return JsonResponse({'code': '5001', 'errormsg': '发送失败'})


class CheckSmsCode(View):

    def get(self, request, phone):
        # 1 接收请求参数
        smscode_client = request.GET.get('smscode', '')

        # 2 校验参数
        if not all([phone, smscode_client]):
            return JsonResponse({'code': '4001', 'errormsg': '缺少必传参数'})

        # 查询服务器短信验证码
        redis_coon = django_redis.get_redis_connection('verify_code')
        smscode_server = redis_coon.get('sms_%s' % phone)

        # 3 匹配
        if not smscode_server:
            return JsonResponse({'code': '4002', 'errormsg': '短信验证码失效'})
        smscode_server = smscode_server.decode('utf8')
        if smscode_server != smscode_client:
            return JsonResponse({'code': '4003', 'errormsg': '验证码不一致'})

        # 4 响应结果
        return JsonResponse({'code': '200', 'errormsg': 'OK'})
