# Generated by Django 2.2.16 on 2021-12-25 08:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('reviews', '0002_auto_20211222_1839'), ('reviews', '0003_auto_20211223_2346'), ('reviews', '0004_auto_20211224_0735'), ('reviews', '0005_auto_20211225_1114')]

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['pk']},
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='unique review'),
        ),
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
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(2021)]),
        ),
    ]