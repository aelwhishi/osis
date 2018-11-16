# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-11-16 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attribution', '0036_auto_20181105_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribution',
            name='function',
            field=models.CharField(blank=True, choices=[('COORDINATOR', 'Coordinator'), ('HOLDER', 'Holder'), ('CO_HOLDER', 'Co-holder'), ('DEPUTY', 'Deputy'), ('DEPUTY_AUTHORITY', 'Deputy authority'), ('DEPUTY_SABBATICAL', 'Deputy sabbatical'), ('DEPUTY_TEMPORARY', 'Deputy temporary'), ('PROFESSOR', 'Professor'), ('INTERNSHIP_SUPERVISOR', 'Internship supervisor'), ('INTERNSHIP_CO_SUPERVISOR', 'Internship co-supervisor')], db_index=True, max_length=35, null=True),
        ),
        migrations.AlterField(
            model_name='attributionnew',
            name='function',
            field=models.CharField(choices=[('COORDINATOR', 'Coordinator'), ('HOLDER', 'Holder'), ('CO_HOLDER', 'Co-holder'), ('DEPUTY', 'Deputy'), ('DEPUTY_AUTHORITY', 'Deputy authority'), ('DEPUTY_SABBATICAL', 'Deputy sabbatical'), ('DEPUTY_TEMPORARY', 'Deputy temporary'), ('PROFESSOR', 'Professor'), ('INTERNSHIP_SUPERVISOR', 'Internship supervisor'), ('INTERNSHIP_CO_SUPERVISOR', 'Internship co-supervisor')], db_index=True, max_length=35, verbose_name='Function'),
        ),
        migrations.AlterField(
            model_name='attributionnew',
            name='start_year',
            field=models.IntegerField(blank=True, null=True, verbose_name='Start'),
        ),
        migrations.AlterField(
            model_name='tutorapplication',
            name='function',
            field=models.CharField(blank=True, choices=[('COORDINATOR', 'Coordinator'), ('HOLDER', 'Holder'), ('CO_HOLDER', 'Co-holder'), ('DEPUTY', 'Deputy'), ('DEPUTY_AUTHORITY', 'Deputy authority'), ('DEPUTY_SABBATICAL', 'Deputy sabbatical'), ('DEPUTY_TEMPORARY', 'Deputy temporary'), ('PROFESSOR', 'Professor'), ('INTERNSHIP_SUPERVISOR', 'Internship supervisor'), ('INTERNSHIP_CO_SUPERVISOR', 'Internship co-supervisor')], db_index=True, max_length=35, null=True),
        ),
    ]
