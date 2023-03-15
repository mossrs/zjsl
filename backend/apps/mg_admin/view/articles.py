from rest_framework.permissions import IsAdminUser
from rest_framework.settings import settings
from fdfs_client.client import get_tracker_conf, Fdfs_client
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.newsapp.models import Article, NewsCategory, ArticleImage, NewsChannel
from ..utils import PageNumPagination
from ..serializers.article import ArticleSerializer, CategorySerializer, ArticleImageSerializer, ChannelSerializer
from rest_framework.filters import SearchFilter


class ArticleViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    pagination_class = PageNumPagination
    queryset = Article.objects.order_by('-id')
    serializer_class = ArticleSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'content']


class ArticleImageViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    pagination_class = PageNumPagination
    queryset = ArticleImage.objects.order_by('-id')
    serializer_class = ArticleImageSerializer
    filter_backends = [SearchFilter]
    # 当从表有外键字段时 需要主表__id 一般是绑定id
    search_fields = ['article__id', 'image']

    def create(self, request, *args, **kwargs):
        """新增图片信息 因为在序列化的时候容易出现一些错误(人为上传)"""
        # 校验
        if all(request.data.values()):
            print(request.data)
            img_name = request.data.get('file').name
            # 手动上传图片
            tracker_path = get_tracker_conf(settings.FASTDFS_CONFIG_PATH)
            # print(tracker_path)
            client = Fdfs_client(tracker_path)
            # 这个方法 因为用户上传肯定是字节数据 所以要用buffer 并read出字节数据
            ret = client.upload_by_buffer(request.data.get('file').read())
            # print(ret)
            # 判断是否成功
            if ret.get('Status') != 'Upload successed.':
                return Response(status=status.HTTP_403_FORBIDDEN)
            img_url = ret.get('Remote file_id').decode('utf-8')
            # 入库操作
            article_img = ArticleImage.objects.create(article_id=request.data['article'], image=img_url)
            Article.objects.filter(id=request.data['article']).update(default_img=img_url)

            # 成功返回
            return Response({
                'id': article_img.id,
                'article': article_img.article_id,
                'image': article_img.image.url,
                'filename': img_name,
            }, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """修改图片信息"""
        if all(request.data.values()):
            img_name = request.data['file'].name
            tracker_path = get_tracker_conf(settings.FASTDFS_CONFIG_PATH)
            client = Fdfs_client(tracker_path)
            ret = client.upload_by_buffer(request.data['file'].read())
            if ret.get('Status') != 'Upload successed.':
                return Response(status=status.HTTP_403_FORBIDDEN)
            img_url = ret.get('Remote file_id').decode('utf-8')
            # 修改当前数据
            article_img = self.get_object()
            article_img.article_id = request.data['article']
            article_img.image = img_url
            return Response({
                'id': article_img.id,
                'article': article_img.article_id,
                'image': article_img.image.url,
                'filename': img_name
            }, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CategoryView(ListAPIView):
    queryset = NewsCategory.objects.all()
    serializer_class = CategorySerializer


class ChannelView(ListAPIView):
    queryset = NewsChannel.objects.all()
    serializer_class = ChannelSerializer
