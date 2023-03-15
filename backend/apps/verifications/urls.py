from django.urls import *
from .views import *

urlpatterns = [
    re_path('^imgcodes/(?P<uuid>[\w-]+)/$', ImgCodeView.as_view()),
    re_path('^smscodes/(?P<phone>1[35789][0-9]{9})/$', SmsCodeView.as_view()),
    re_path('^check_smscode/(?P<phone>1[35789][0-9]{9})/$', CheckSmsCode.as_view()),

]
