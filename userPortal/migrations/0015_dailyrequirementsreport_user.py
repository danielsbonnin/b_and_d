# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-25 22:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userPortal', '0014_dailyrequirementsreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyrequirementsreport',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
