# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-13 20:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0044_user_notify_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='notify_email',
        ),
    ]