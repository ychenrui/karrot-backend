# Generated by Django 4.2.7 on 2024-01-25 14:19

from django.db import migrations
import karrot.base.base_models
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0050_enable_agreements_and_participant_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='photo',
            field=versatileimagefield.fields.VersatileImageField(null=True, upload_to=karrot.base.base_models.UploadToUUID('group_photos'), verbose_name='Group Photo'),
        ),
    ]