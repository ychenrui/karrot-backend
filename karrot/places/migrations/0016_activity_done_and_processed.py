# Generated by Django 1.11.4 on 2017-08-10 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0015_auto_20170727_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='done_and_processed',
            field=models.BooleanField(default=False),
        ),
    ]
