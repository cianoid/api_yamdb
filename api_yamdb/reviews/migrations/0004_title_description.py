# Generated by Django 2.2.16 on 2021-12-18 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20211216_1858_squashed_0004_auto_20211216_1905'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
