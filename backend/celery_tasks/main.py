from celery import *

# 创建celery 实例
celery_app = Celery('poetry')

# 加载配置文件
celery_app.config_from_object('celery_tasks.config')

# 注册celery任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])

