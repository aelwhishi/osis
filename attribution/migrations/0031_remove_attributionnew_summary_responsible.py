# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-03-28 12:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attribution', '0030_auto_20180228_0856'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attributionnew',
            name='summary_responsible',
        ),
    ]
