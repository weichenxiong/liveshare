# Generated by Django 2.2 on 2020-05-30 07:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='article',
            table='live_article',
        ),
        migrations.AlterModelTable(
            name='articlecollection',
            table='live_article_collection',
        ),
        migrations.AlterModelTable(
            name='articleimage',
            table='live_article_image',
        ),
        migrations.AlterModelTable(
            name='special',
            table='live_special',
        ),
        migrations.AlterModelTable(
            name='specialarticle',
            table='live_special_article',
        ),
        migrations.AlterModelTable(
            name='specialcollection',
            table='live_special_collection',
        ),
        migrations.AlterModelTable(
            name='specialfocus',
            table='live_special_focus',
        ),
        migrations.AlterModelTable(
            name='specialmanager',
            table='live_special_manager',
        ),
    ]
