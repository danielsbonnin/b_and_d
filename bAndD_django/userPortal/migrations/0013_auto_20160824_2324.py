# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-25 04:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userPortal', '0012_child_no_screens_until'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpdateEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(blank=True, null=True)),
                ('amount', models.IntegerField(default=0)),
                ('reason', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='child',
            options={'verbose_name_plural': 'children'},
        ),
    ]