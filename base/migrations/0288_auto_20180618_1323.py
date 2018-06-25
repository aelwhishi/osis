# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-06-18 11:23
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0287_auto_20180615_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externallearningunityear',
            name='url',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='url of the learning unit'),
        ),
        migrations.AlterField(
            model_name='learningunityear',
            name='credits',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(500)], verbose_name='credits'),
        ),
    ]