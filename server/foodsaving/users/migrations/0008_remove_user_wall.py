# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-30 08:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20161224_1706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='wall',
        ),
        migrations.RemoveField(
            model_name='user',
            name='profile_visibility'
        )
    ]
