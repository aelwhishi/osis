# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-12-10 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0410_auto_20181207_1523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='educationgrouppublicationcontact',
            name='role',
        ),
        migrations.AddField(
            model_name='educationgrouppublicationcontact',
            name='description',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='educationgrouppublicationcontact',
            name='role_en',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='role in english'),
        ),
        migrations.AddField(
            model_name='educationgrouppublicationcontact',
            name='role_fr',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='role in french'),
        ),
    ]