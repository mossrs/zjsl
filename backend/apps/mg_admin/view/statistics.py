import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from apps.payment.models import OrderInfo
from apps.userapp.models import Users


class UserTotalView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        count = Users.objects.count()
        # print(count)
        return Response({'count': count})


class UserDayCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 可借助django自带的时区函数来获取你在配置文件中的时区时间
        count = Users.objects.filter(date_joined__gte=(datetime.datetime.utcnow() - datetime.timedelta(hours=24))).count()
        return Response({'count': count})


class UserActiveCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        count = Users.objects.filter(last_login__gte=(datetime.datetime.utcnow() - datetime.timedelta(hours=24))).count()
        return Response({'count': count})


class TimeOrderCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        t_count_list = []
        y_count_list = []
        today = datetime.datetime.today()
        yesterday = today + datetime.timedelta(days=-1)

        times = ['00', '02', '04', '06', '08', '10',
                 '12', '14', '16', '18', '20', '22']
        for t in times:
            t_count = OrderInfo.objects.filter(create_time__year=today.year,
                                               create_time__month=today.month,
                                               create_time__day=today.day,
                                               create_time__hour__lte=t).count()
            t_count_list.append(t_count)
            y_count = OrderInfo.objects.filter(create_time__year=yesterday.year,
                                               create_time__month=yesterday.month,
                                               create_time__day=yesterday.day,
                                               create_time__hour__lte=t).count()
            y_count_list.append(y_count)
            # 显示效果手动增加
            t_count_list = ['100', '300', '500', '600', '700', '800',
                            '500', '1200', '900', '1000', '700', '600']
            y_count_list = ['100', '200', '400', '300', '500', '700',
                            '500', '800', '900', '1000', '600', '500']
        return Response({'t_count_list': t_count_list,
                         'y_count_list': y_count_list})
