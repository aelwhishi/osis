# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-04-23 18:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0448_delete_components_without_learning_units'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='learningcomponentyear',
            name='learning_container_year',
        ),
        migrations.AlterField(
            model_name='learningcomponentyear',
            name='learning_unit_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.LearningUnitYear'),
            preserve_default=False,
        ),
    ]
