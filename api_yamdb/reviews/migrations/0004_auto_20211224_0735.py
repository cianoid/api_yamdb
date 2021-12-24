# Generated by Django 2.2.16 on 2021-12-24 04:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20211223_2346'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('pk',), 'verbose_name': 'категорию', 'verbose_name_plural': 'категории'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-pub_date',), 'verbose_name': 'комментарий', 'verbose_name_plural': 'комментарии'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ('pk',), 'verbose_name': 'жанр', 'verbose_name_plural': 'жанры'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('-pub_date',), 'verbose_name': 'ревью', 'verbose_name_plural': 'ревью'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ('pk',), 'verbose_name': 'произведение', 'verbose_name_plural': 'произведения'},
        ),
    ]
