# Generated by Django 2.2 on 2020-06-13 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0008_article_pub_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='pub_status',
        ),
    ]
