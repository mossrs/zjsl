from urllib.request import urlopen
from urllib.parse import urlencode
from django.conf import settings
import json


def send_sms_code(smscode, phone):
    # APIID(用户中心【验证码通知短信】-【产品纵览】查看)
    account = settings.APIID
    # APIKEY(用户中心【验证码通知短信】-【产品纵览】查看)
    password = settings.APIKEY
    text = "您的验证码是：%s。请不要把验证码泄露给其他人。" % smscode
    data = {'account': account, 'password': password, 'content': text, 'mobile': phone, 'format': 'json'}
    req = urlopen(url='https://106.ihuyi.com/webservice/sms.php?method=Submit', data=urlencode(data).encode())
    content = req.read().decode()
    print(content)
    # code等于2代表提交成功，否则提交失败
    # smsid等于0代表提交失败，否则显示长度20流水号
    # b'{"code":2,"msg":"\xe6\x8f\x90\xe4\xba\xa4\xe6\x88\x90\xe5\x8a\x9f","smsid":"16063783563405105174"}'

    return json.loads(content)

#
# def send_sms_code(text, mobile):
#     host = "106.ihuyi.com"
#     sms_send_uri = "/webservice/sms.php?method=Submit"
#     account = settings.APIID
#     password = settings.APIKEY
#     data = {'account': account, 'password': password, 'content': text, 'mobile': mobile, 'format': 'json'}
#     params = urlencode(data)
#     headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
#     conn = httplib2.HTTPConnectionWithTimeout(host, port=80, timeout=30)
#     conn.request('POST', sms_send_uri, params, headers)
#     response = conn.getresponse()
#     print(response, type(response))
#     conn.close()
#     return response














