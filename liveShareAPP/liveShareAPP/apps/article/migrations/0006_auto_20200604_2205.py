# Generated by Django 2.2 on 2020-06-04 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_auto_20200602_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleimage',
            name='link',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='图片地址'),
        ),
    ]
