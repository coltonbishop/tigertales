# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-22 00:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_book_puid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='amazon_price',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='book',
            name='lab_price',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='book',
            name='puid',
            field=models.TextField(),
        ),
    ]
