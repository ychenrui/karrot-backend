# Generated by Django 3.0.9 on 2020-08-20 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0020_activity_feedback_always_as_sum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='feedback_as_sum',
        ),
    ]