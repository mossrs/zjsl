from django.urls import *
from apps.userapp.views import *
from django.contrib.auth.decorators import *


urlpatterns = [
    # as.view() 方法可以将类试图转变成函数视图 再次加装饰器即可修饰
    re_path('^register/$', RegisterView.as_view()),
    re_path('^usernames/(?P<username>[a-zA-Z_]{5,8})/count/$', UsernameCountView.as_view()),
    re_path('^phones/(?P<phone>1[35789][0-9]{9})/count/$', PhoneCountView.as_view()),
    re_path('^logout/$', LogoutView.as_view()),
    re_path('^login/$', LoginView.as_view()),
    re_path('^usercenter/$', login_required(UserCenterView.as_view())),
    re_path('^emails/$', EmailsView.as_view()),

]
