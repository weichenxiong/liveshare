# Generated by Django 2.2 on 2020-05-31 09:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0003_article_save_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticlePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orders', models.IntegerField(blank=True, default=0, null=True, verbose_name='排序')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否展示')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('status', models.IntegerField(choices=[(0, '未审核'), (1, '审核通过'), (2, '审核未通过')], default=0, verbose_name='审核状态')),
                ('manager', models.IntegerField(blank=True, default=None, null=True, verbose_name='审核人')),
                ('post_time', models.DateTimeField(blank=True, default=None, null=True, verbose_name='审核时间')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Article', verbose_name='文章')),
                ('special', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Special', verbose_name='专题')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='投稿人')),
            ],
            options={
                'verbose_name': '文章的投稿记录',
                'verbose_name_plural': '文章的投稿记录',
                'db_table': 'live_article_post',
            },
        ),
    ]
