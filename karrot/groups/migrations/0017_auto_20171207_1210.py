# Generated by Django 1.11.7 on 2017-12-07 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0016_auto_20171101_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='active_agreement',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='active_group', to='groups.Agreement'),
        ),
    ]
