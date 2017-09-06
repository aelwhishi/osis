# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-06 14:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0151_remove_learningunit_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academiccalendar',
            name='highlight_title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='learningunityear',
            name='session',
            field=models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('12', '12'), ('13', '13'), ('23', '23'), ('123', '123'), ('P23', 'P23')], max_length=50, null=True),
        ),
    ]
