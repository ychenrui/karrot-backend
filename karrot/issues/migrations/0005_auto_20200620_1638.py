# Generated by Django 3.0.2 on 2020-06-20 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0004_enable_issue_notifications'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='participants',
        ),
        migrations.DeleteModel(
            name='IssueParticipant',
        ),
    ]