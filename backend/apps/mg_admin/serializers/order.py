from rest_framework.serializers import ModelSerializer
from apps.payment.models import OrderInfo


class OrderSerializer(ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = '__all__'
