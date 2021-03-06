# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-09-21 10:59
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0357_auto_20180920_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='educationgroupachievement',
            name='english_text',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='text in English'),
        ),
        migrations.AddField(
            model_name='educationgroupachievement',
            name='french_text',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='text in French'),
        ),
        migrations.AddField(
            model_name='educationgroupdetailedachievement',
            name='english_text',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='text in English'),
        ),
        migrations.AddField(
            model_name='educationgroupdetailedachievement',
            name='french_text',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='text in French'),
        ),
        migrations.AlterUniqueTogether(
            name='educationgroupachievement',
            unique_together=set([('code_name', 'education_group_year')]),
        ),

        migrations.AlterUniqueTogether(
            name='educationgroupdetailedachievement',
            unique_together=set([('code_name', 'education_group_achievement')]),
        ),
        migrations.RemoveField(
            model_name='educationgroupachievement',
            name='language',
        ),
        migrations.RemoveField(
            model_name='educationgroupachievement',
            name='text',
        ),
        migrations.RemoveField(
            model_name='educationgroupdetailedachievement',
            name='language',
        ),
        migrations.RemoveField(
            model_name='educationgroupdetailedachievement',
            name='text',
        ),
    ]
