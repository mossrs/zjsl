from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.mg_admin.utils import PageNumPagination
from apps.payment.models import OrderInfo
from ..serializers.order import OrderSerializer
from rest_framework.status import HTTP_200_OK


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    pagination_class = PageNumPagination
    queryset = OrderInfo.objects.order_by('-create_time')
    serializer_class = OrderSerializer
    filter_backends = [SearchFilter]
    search_fields = ['user__id', 'create_time', 'pay_method', 'total_amount', 'article__id', 'order_id']

    @action(methods=['put'], detail=True)
    def status(self, request, pk):
        status = request.data.get('status')
        order_obj = self.get_object()
        order_obj.status = status
        order_obj.save()

        return Response({
            'order_id': order_obj.order_id,
            'status': order_obj.status
        }, status=HTTP_200_OK)
