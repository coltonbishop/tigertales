# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-05-01 19:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_auto_20180501_1827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='saved_by',
        ),
        migrations.AddField(
            model_name='cart',
            name='saved_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.User'),
            preserve_default=False,
        ),
    ]
