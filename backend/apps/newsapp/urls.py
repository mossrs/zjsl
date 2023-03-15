from django.urls import *
from apps.newsapp.views import *

urlpatterns = [
    re_path('^$', IndexView.as_view(), name='index'),
    re_path('^dayunhe/$', DaYunHeView.as_view(), name='dayunhe'),
    re_path('^qiantangjiang/$', QianTangJiangView.as_view(), name='qiantangjiang'),
    re_path('^oujiangshanshui/$', OuJiangShanShuiView.as_view(), name='oujiangshanshui'),
    re_path('^zhedong/$', ZheDongTangShiView.as_view(), name='zhedong'),
    re_path('^list/(?P<channel_id>\d+)/(?P<page_num>\d+)/$', IndexView.as_view()),
    re_path('^dayunhelist/(?P<dachannel_id>\d+)/(?P<page_num>\d+)/$', DaYunHeView.as_view()),
    re_path('^qiantanglist/(?P<channel_id>\d+)/(?P<page_num>\d+)/$', QianTangJiangView.as_view()),
    re_path('^oujianglist/(?P<channel_id>\d+)/(?P<page_num>\d+)/$', OuJiangShanShuiView.as_view()),
    re_path('^zhedonglist/(?P<channel_id>\d+)/(?P<page_num>\d+)/$', ZheDongTangShiView.as_view()),
    re_path('^comment_control/$', CommentControl.as_view()),
    re_path('^search/', include('haystack.urls')),
    re_path('^detail/(?P<article_id>\d+)/$', DetailView.as_view()),
]
