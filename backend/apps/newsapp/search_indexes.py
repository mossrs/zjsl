from haystack import indexes
from .models import *


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    """
        Article的索引数据模型类
    """
    # 使用模板会默认找templates/search/indexes/youapp/\<model_name>_text.txt
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        """
            返回建立索引的模型类
        """
        return Article

    def index_queryset(self, using=None):
        """
            返回要建立索引的数据库查询集
        """
        return self.get_model().objects.order_by('-id')
