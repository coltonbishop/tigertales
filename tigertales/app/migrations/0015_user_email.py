# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-27 16:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20180427_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.CharField(default='', max_length=250),
        ),
    ]
