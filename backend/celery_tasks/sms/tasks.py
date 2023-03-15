# 这个异步任务的模块名必须是 tasks 因为源码里对应的是tasks 也可以改
# 添加导包路路径
import os
import sys

B_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(1, B_DIR)
sys.path.insert(0, os.path.join(B_DIR, 'utils'))

import logging
from celery_tasks.main import celery_app
from utils.huyi_sms.sms3 import send_sms_code

# 为celery使⽤用django配置⽂文件进⾏行行设置
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portey_road.settings')

logger = logging.getLogger('django')


@celery_app.task(name='huyi_send_sms_code')
def huyi_send_sms_code(phone, smscode_str):
    ret = ''
    e = ''
    try:
        # 调⽤用外部接⼝口执⾏行行发送短信任务
        ret = send_sms_code(smscode_str, phone)
    except Exception as e:
        logger.error(e)
    if ret.get('code') != 2:
        logger.error(e)
    return ret.get('code', None)
