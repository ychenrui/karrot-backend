# Generated by Django 1.10.4 on 2017-02-23 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0010_auto_20170214_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=80, unique=True),
        ),
    ]
