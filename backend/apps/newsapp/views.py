from django import http
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.core.paginator import *


class IndexView(View):

    def get(self, request, channel_id=1, page_num=1):
        # 注意这里重定向模板因为定义过模板语言了 所以就可以直接导入对应的模板
        """
            动态渲染诗路列表
        """
        # # 获取当前频道下的所有类别
        # try:
        #     news_channel = NewsChannel.objects.get(id=channel_id)
        # except:
        #     return http.HttpResponseNotFound('未找到频道id')
        # else:
        #     category_list = [category.id for category in news_channel.newscategory_set.all() if category]
        #
        # # 查看当前频道的所有文章
        # articles = Article.objects.filter(category_id__in=category_list).order_by('-id')
        articles = Article.objects.all().order_by('id')
        # 创建分页器对象
        page_obj = Paginator(articles, 3)
        # 获取当前页数据
        try:
            page_articles = page_obj.page(page_num)
        except EmptyPage:
            return http.HttpResponseNotFound('为找到相应的page_num')

        # 注意 这个返回给模板的上下文对象 在jinja2中是通过键名来点语法的 而不是值名 切忌传给jinja2模板中的值是按照 字典里的‘值’点语法的
        return render(request, 'newsapp/index.html', {'page_articles': page_articles,
                                                      'channel_id': channel_id})


class DetailView(View):
    """
        诗路详情
    """

    def get(self, request, article_id):
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExit:
            return http.HttpResponseNotFound('未找到相应诗路')
        return render(request, 'newsapp/detail.html', {'article': article})


class DaYunHeView(View):
    def get(self, request, page_num=1, dachannel_id=1):
        articles = Article.objects.filter(channel_id=1).order_by('id')
        # 创建分页器对象
        page_obj = Paginator(articles, 3)
        # 获取当前页数据
        try:
            page_articles = page_obj.page(page_num)
        except EmptyPage:
            return http.HttpResponseNotFound('为找到相应的page_num')

        # 注意 这个返回给模板的上下文对象 在jinja2中是通过键名来点语法的 而不是值名
        return render(request, 'newsapp/channel/dayunhe.html', {'page_articles': page_articles,
                                                                'dachannel_id': dachannel_id})


class QianTangJiangView(View):
    def get(self, request, page_num=1, channel_id=2):
        articles = Article.objects.filter(channel_id=2).order_by('id')
        # 创建分页器对象
        page_obj = Paginator(articles, 3)
        # 获取当前页数据
        try:
            page_articles = page_obj.page(page_num)
        except EmptyPage:
            return http.HttpResponseNotFound('为找到相应的page_num')

        # 注意 这个返回给模板的上下文对象 在jinja2中是通过键名来点语法的 而不是值名
        return render(request, 'newsapp/channel/qiantangjiang.html', {'page_articles': page_articles,
                                                                      'channel_id': channel_id})


class OuJiangShanShuiView(View):
    def get(self, request, page_num=1, channel_id=3):
        articles = Article.objects.filter(channel_id=3).order_by('id')
        # 创建分页器对象
        page_obj = Paginator(articles, 3)
        # 获取当前页数据
        try:
            page_articles = page_obj.page(page_num)
        except EmptyPage:
            return http.HttpResponseNotFound('为找到相应的page_num')

        # 注意 这个返回给模板的上下文对象 在jinja2中是通过键名来点语法的 而不是值名
        return render(request, 'newsapp/channel/oujiangshanshui.html', {'page_articles': page_articles,
                                                                        'channel_id': channel_id})


class ZheDongTangShiView(View):
    def get(self, request, page_num=1, channel_id=4):
        articles = Article.objects.filter(channel_id=4).order_by('id')
        # 创建分页器对象
        page_obj = Paginator(articles, 3)
        # 获取当前页数据
        try:
            page_articles = page_obj.page(page_num)
        except EmptyPage:
            return http.HttpResponseNotFound('为找到相应的page_num')

        # 注意 这个返回给模板的上下文对象 在jinja2中是通过键名来点语法的 而不是值名
        return render(request, 'newsapp/channel/zhedongtangshi.html', {'page_articles': page_articles,
                                                                       'channel_id': channel_id})


class CommentControl(View):
    def post(self, request):
        if request.user.username:
            comment_content = request.POST.get('comment_content')
            article_id = request.POST.get('article_id')
            pid = request.POST.get('pid')
            author_id = request.user.id
            Comment.objects.create(comment_content=comment_content, pre_comment_id=pid,
                                   article_id=article_id, comment_author_id=author_id)
            return HttpResponse(status=200)
        return redirect('/login/')
