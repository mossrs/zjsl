from django.contrib.auth.models import *


class Users(AbstractUser):
    phone = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    class Meta:
        db_table = 't_user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
