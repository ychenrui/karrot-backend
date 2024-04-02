# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-28 17:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_auto_20160721_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='address',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='place',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='place',
            name='longitude',
            field=models.FloatField(null=True),
        ),
    ]
