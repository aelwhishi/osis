# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-12-10 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0415_auto_20181212_0821'),
    ]

    operations = [
        migrations.AddField(
            model_name='educationgrouptype',
            name='learning_unit_child_allowed',
            field=models.BooleanField(default=False),
        ),
    ]