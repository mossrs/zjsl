from django.db import models
from apps.userapp.models import Users
from utils.basemodels import BaseModel
from apps.newsapp.models import Article


class OrderInfo(BaseModel):
    PAY_METHOD_CHOICES = (
        (1, '支付宝'),
        (2, '微信'),
    )
    ORDER_STATUS_CHOICES = (
        (1, '待支付'),
        (2, '已完成'),
        (3, '已取消'),
    )
    order_id = models.CharField(max_length=64, primary_key=True, verbose_name='订单号')
    user = models.ForeignKey(Users, on_delete=models.PROTECT, verbose_name='下单用户')
    # decimal_places 小数的最大位数    max_digits 最大位数
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单总金额')
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=1, verbose_name='支付方式')
    status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name='订单状态')
    article = models.ForeignKey(Article, on_delete=models.PROTECT, verbose_name='订单文章')

    class Meta:
        db_table = 't_order_info'
        verbose_name = '订单基本信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_id


class Payment(BaseModel):
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name='订单')
    trade_id = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='支付编号')

    class Meta:
        db_table = 't_payment'
        verbose_name = '支付信息'
        verbose_name_plural = verbose_name
