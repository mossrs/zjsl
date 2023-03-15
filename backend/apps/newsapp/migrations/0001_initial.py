# Generated by Django 2.2 on 2022-01-20 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='⽂章标题')),
                ('content', models.TextField(verbose_name='⽂章内容')),
                ('default_img', models.ImageField(upload_to='', verbose_name='⾸⻚图⽚')),
                ('starcount', models.IntegerField(default=0, verbose_name='点赞量')),
                ('commentcount', models.IntegerField(default=0, verbose_name='评论量')),
            ],
            options={
                'verbose_name': '⽂章',
                'verbose_name_plural': '⽂章',
                'db_table': 't_news_article',
            },
        ),
        migrations.CreateModel(
            name='NewsChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='频道名称')),
                ('url', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='频道⻚⾯链接')),
            ],
            options={
                'verbose_name': '新闻频道',
                'verbose_name_plural': '新闻频道',
                'db_table': 't_news_channel',
            },
        ),
        migrations.CreateModel(
            name='NewsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=10, verbose_name='名称')),
                ('sequence', models.IntegerField(verbose_name='排序')),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='newsapp.NewsChannel')),
            ],
            options={
                'verbose_name': '新闻类别',
                'verbose_name_plural': '新闻类别',
                'db_table': 't_news_category',
            },
        ),
        migrations.CreateModel(
            name='ArticleImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('image', models.ImageField(upload_to='', verbose_name='图⽚')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsapp.Article')),
            ],
            options={
                'verbose_name': 'article图⽚',
                'verbose_name_plural': 'article图⽚',
                'db_table': 't_article_image',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='newsapp.NewsCategory', verbose_name='从属类别'),
        ),
    ]