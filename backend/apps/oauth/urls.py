from django.urls import re_path
from .views import *


urlpatterns = [
    re_path('^qq/login/$', QQLoginView.as_view()),
    re_path('^about/$', QQAuthUserView.as_view()),

]
