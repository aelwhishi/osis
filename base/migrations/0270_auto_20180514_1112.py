# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-14 09:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0269_learningcomponentyear_tp_to_pp'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='entitycontaineryear',
            unique_together=set([('learning_container_year', 'type')]),
        ),
    ]
