from apps.newsapp.models import Article, NewsCategory, ArticleImage, NewsChannel
from rest_framework import serializers


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'starcount', 'commentcount', 'category', 'channel']

    def create(self, validated_data):
        """新增诗路信息"""
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.starcount = validated_data.get('starcount', instance.starcount)
        instance.commentcount = validated_data.get('commentcount', instance.commentcount)
        instance.category = validated_data.get('category', instance.category)
        instance.channel = validated_data.get('channel', instance.channel)
        instance.save()
        return instance


class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        # 这个字段就可以直接按照你模型类里的写就行
        fields = ['id', 'article', 'image']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ['id', 'name']


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsChannel
        fields = ['id', 'name']

