# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-22 00:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20180422_0051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='puid',
        ),
    ]