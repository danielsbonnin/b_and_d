# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-01 19:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userPortal', '0024_auto_20160901_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyrequirementsreport',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_reports', to=settings.AUTH_USER_MODEL),
        ),
    ]
