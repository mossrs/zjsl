"""portey_road URL Configuration

The `urlpatterns` list routes URLs to view. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function view
    1. Add an import:  from my_app import view
    2. Add a URL to urlpatterns:  path('', view.home, name='home')
Class-based view
    1. Add an import:  from other_app.view import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.utils import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.utils'))
"""
from django.contrib import admin
from django.urls import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # 配置根路由 我们一般都使用namespace所以include里第一个参数是元组（指定子路由，子应用名）
    re_path('^', include('apps.userapp.urls')),
    re_path('^', include(('apps.newsapp.urls', 'apps.newsapp'), namespace='newsapp')),
    re_path('^', include(('apps.verifications.urls', 'apps.verifications'), namespace='verifications')),
    re_path('^', include('apps.oauth.urls')),
    re_path('^', include('apps.payment.urls'), ),
    re_path('^', include('apps.mg_admin.urls')),


]
