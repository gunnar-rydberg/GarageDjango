# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-05 12:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garage_app', '0004_auto_20171105_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='vehicle_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='garage_app.VehicleType'),
            preserve_default=False,
        ),
    ]
