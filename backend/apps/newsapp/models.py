from django.db import models

from apps.userapp.models import Users
from utils.basemodels import BaseModel


class NewsChannel(BaseModel):
    """诗路频道"""

    name = models.CharField(max_length=30, unique=True, verbose_name='频道名称')
    url = models.CharField(default='', null=True, blank=True, max_length=50,
                           verbose_name='频道⻚⾯链接')

    class Meta:
        db_table = 't_news_channel'
        verbose_name = '诗路频道'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class NewsCategory(BaseModel):
    """诗路类别"""

    name = models.CharField(max_length=10, verbose_name='名称')
    sequence = models.IntegerField(verbose_name='排序')
    channel = models.ForeignKey(NewsChannel, on_delete=models.PROTECT)

    class Meta:
        db_table = 't_news_category'
        verbose_name = '诗路类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Article(BaseModel):
    """⽂章"""

    title = models.CharField(max_length=100, unique=True, verbose_name='⽂章标题')
    content = models.TextField(verbose_name='⽂章内容')
    default_img = models.ImageField(verbose_name='⾸⻚图⽚')
    starcount = models.IntegerField(default=0, verbose_name='点赞量')
    commentcount = models.IntegerField(default=0, verbose_name='评论量')
    category = models.ForeignKey(NewsCategory, on_delete=models.PROTECT,
                                 verbose_name='从属类别')
    channel = models.ForeignKey(NewsChannel, on_delete=models.PROTECT, verbose_name='从属诗路')

    class Meta:
        db_table = 't_news_article'
        verbose_name = '⽂章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class ArticleImage(BaseModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='图⽚')

    class Meta:
        db_table = 't_article_image'
        verbose_name = 'article图⽚'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s' % (self.article.title, self.id)


class Comment(BaseModel):
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, verbose_name='评论文章')
    comment_content = models.TextField(verbose_name='评论文章')
    comment_author = models.ForeignKey(Users, on_delete=models.DO_NOTHING, verbose_name='评论人')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    pre_comment = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, verbose_name='父评论id')

    class Meta:
        db_table = 't_comment'
        verbose_name = '评论表'
        verbose_name_plural = verbose_name

