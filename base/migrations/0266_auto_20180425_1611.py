# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-04-25 14:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0265_educationgroupyear_credits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learningcontaineryear',
            name='is_vacant',
            field=models.BooleanField(default=False, verbose_name='vacant'),
        ),
        migrations.AlterField(
            model_name='learningcontaineryear',
            name='team',
            field=models.BooleanField(default=False, verbose_name='team_management'),
        ),
        migrations.AlterField(
            model_name='learningcontaineryear',
            name='type_declaration_vacant',
            field=models.CharField(blank=True, choices=[('RESEVED_FOR_INTERNS', 'RESEVED_FOR_INTERNS'), ('OPEN_FOR_EXTERNS', 'OPEN_FOR_EXTERNS'), ('EXCEPTIONAL_PROCEDURE', 'EXCEPTIONAL_PROCEDURE'), ('VACANT_NOT_PUBLISH', 'VACANT_NOT_PUBLISH'), ('DO_NOT_ASSIGN', 'DO_NOT_ASSIGN')], max_length=100, null=True, verbose_name='type_declaration_vacant'),
        ),
        migrations.AlterField(
            model_name='learningunityear',
            name='attribution_procedure',
            field=models.CharField(blank=True, choices=[('INTERNAL_TEAM', 'INTERNAL_TEAM'), ('EXTERNAL', 'EXTERNAL')], max_length=20, null=True, verbose_name='procedure'),
        ),
    ]
