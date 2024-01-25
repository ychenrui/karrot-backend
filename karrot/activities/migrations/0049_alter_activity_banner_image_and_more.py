# Generated by Django 4.2.7 on 2024-01-25 14:04

from django.db import migrations
import karrot.activities.models
import versatileimagefield.fields

import karrot.base.base_models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0048_activityseries_banner_image_activityseries_is_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='banner_image',
            field=versatileimagefield.fields.VersatileImageField(null=True, upload_to=karrot.base.base_models.UploadToUUID('activity__banner_images'), verbose_name='BannerImage'),
        ),
        migrations.AlterField(
            model_name='activityseries',
            name='banner_image',
            field=versatileimagefield.fields.VersatileImageField(null=True, upload_to=karrot.base.base_models.UploadToUUID('activity_series__banner_images'), verbose_name='BannerImage'),
        ),
    ]
