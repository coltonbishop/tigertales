# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-13 21:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0046_user_notify_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='listings',
        ),
        migrations.RemoveField(
            model_name='shop',
            name='user',
        ),
        migrations.DeleteModel(
            name='Shop',
        ),
    ]
