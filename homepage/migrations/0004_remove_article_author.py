# Generated by Django 3.1 on 2020-10-02 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0003_article_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
    ]
