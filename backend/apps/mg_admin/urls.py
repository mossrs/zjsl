from django.urls import re_path
from rest_framework_jwt.views import obtain_jwt_token
from .view.statistics import *
from .view.users import *
from rest_framework import routers
from .view.articles import ArticleViewSet, CategoryView, ArticleImageViewSet, ChannelView
from .view.orders import OrderViewSet
from .view.systems import PermissionViewSet, GroupViewSet, AdminViewSet

urlpatterns = [
    re_path('^mg_admin/login/$', obtain_jwt_token),
    re_path('^statistics/total_count/$', UserTotalView.as_view()),
    re_path('^statistics/day_increment/$', UserDayCountView.as_view()),
    re_path('^statistics/day_active/$', UserActiveCountView.as_view()),
    re_path('^statistics/time_order_count/$', TimeOrderCountView.as_view()),
    # re_path('^mg_admin/users/$', UsersView.as_view()),
    re_path('^mg_admin/categories/$', CategoryView.as_view()),
    re_path('^mg_admin/channels/$', ChannelView.as_view()),


]

router = routers.SimpleRouter()
router.register('users', UsersViewSet, 'user')
router.register('articles', ArticleViewSet, 'article')
router.register('article_imgs', ArticleImageViewSet, 'article_img')
router.register('orders', OrderViewSet, 'order')
router.register('permissions', PermissionViewSet, 'permission')
router.register('groups', GroupViewSet, 'group')
router.register('admins', AdminViewSet, 'admin')
urlpatterns += router.urls
# print(urlpatterns)
