# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 08:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0016_merge_20171026_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bestilling',
            name='pris',
            field=models.IntegerField(),
        ),
    ]
