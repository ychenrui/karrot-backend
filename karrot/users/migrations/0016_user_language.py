# Generated by Django 1.11 on 2017-05-22 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20170413_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='language',
            field=models.CharField(default='en', max_length=7),
        ),
    ]
