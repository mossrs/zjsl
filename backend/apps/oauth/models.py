from django.db import models
from apps import userapp
from utils.basemodels import BaseModel


class QQAuthUser(BaseModel):
    user = models.ForeignKey('userapp.Users', on_delete=models.CASCADE)
    openid = models.CharField(max_length=64, db_index=True)

    class Meta:
        db_table = 't_qq_auth'
        verbose_name = 'QQ用户登陆数据'
        verbose_name_plural = verbose_name
