# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-30 22:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userPortal', '0022_auto_20160829_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='child',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent', to=settings.AUTH_USER_MODEL),
        ),
    ]
