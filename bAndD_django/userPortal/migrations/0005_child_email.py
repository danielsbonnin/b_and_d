# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-17 00:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userPortal', '0004_auto_20160816_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='child',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
