# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-11-29 09:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0402_date_enrollment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='educationgroup',
            options={'permissions': (('can_access_education_group', 'Can access education_group'), ('can_edit_educationgroup_pedagogy', 'Can edit education group pedagogy'), ('can_edit_common_education_group', 'Can edit common education group'))},
        )
    ]