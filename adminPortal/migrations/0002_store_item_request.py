# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-07 22:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adminPortal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store_item_request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('link', models.CharField(blank=True, max_length=1000, null=True)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
