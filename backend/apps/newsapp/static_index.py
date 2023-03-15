import os
from django.conf import settings
from django.template import loader
from django.utils import timezone
from .models import *
from django.core.paginator import *


def static_index():

    """
        将新闻首页信息静态化处理
    """
    # 准备base.html需要的数据
    channels = NewsChannel.objects.order_by('id')

    news_channel = NewsChannel.objects.get(id=1)

    # 父表可通过查询到的结果然后 子表类名小写_set.all() 来获取子表所有数据
    category_list = [category.id for category in news_channel.newscategory_set.all() if category]

    # 查看当前频道的所有文章
    articles = Article.objects.filter(category_id__in=category_list).order_by('id')

    # 创建分页器对象
    page_obj = Paginator(articles, 3)
    # 获取当前页数据
    page_articles = page_obj.page(1)

    # 准备页面数据
    context = {
        'page_articles': page_articles,
        'channel_id': 1,
        'channels': channels
    }
    template = loader.get_template('newsapp/index.html')
    html_text = template.render(context)
    file_path = os.path.join(settings.STATICFILES_DIRS[0], 'index.html')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_text)
    print(timezone.localtime().strftime('%H:%M:%S'))

