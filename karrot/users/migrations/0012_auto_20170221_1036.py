# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-21 10:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20170215_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='unverified_email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
    ]
