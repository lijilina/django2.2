# Generated by Django 2.2.12 on 2022-03-24 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_test_article_test_publication'),
    ]

    operations = [
        migrations.DeleteModel(
            name='test_Article',
        ),
        migrations.DeleteModel(
            name='test_Publication',
        ),
    ]
