# Generated by Django 1.10.4 on 2016-12-18 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0006_auto_20161211_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='password',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
