# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-13 20:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0043_remove_user_notify_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='notify_email',
            field=models.BooleanField(default=False),
        ),
    ]
