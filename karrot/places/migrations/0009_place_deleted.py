# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-23 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0008_auto_20170220_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
