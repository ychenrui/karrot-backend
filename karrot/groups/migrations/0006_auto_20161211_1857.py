# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-11 18:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0005_auto_20161026_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
    ]