# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-04-16 08:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0255_auto_20180416_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='learningachievements',
            name='changed',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='learningachievements',
            name='external_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]