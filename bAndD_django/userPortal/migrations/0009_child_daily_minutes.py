# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-24 03:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userPortal', '0008_auto_20160817_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='child',
            name='daily_minutes',
            field=models.PositiveSmallIntegerField(blank=True, default=120),
        ),
    ]
