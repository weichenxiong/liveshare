# Generated by Django 2.2 on 2020-06-04 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_auto_20200604_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='article_image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='文章图片'),
        ),
    ]
