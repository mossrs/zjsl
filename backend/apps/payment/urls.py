from django.urls import *
from .views import *
from django.contrib.auth.decorators import *
urlpatterns = [
    re_path('^payment/$', PaymentView.as_view()),
    re_path('^payment/status/$', PaymentStatusView.as_view()),

]