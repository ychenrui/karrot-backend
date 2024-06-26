# Generated by Django 1.11.6 on 2017-10-28 18:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0014_groupmembership_roles'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.TextField()),
                ('content', models.TextField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.Group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserAgreement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('agreement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.Agreement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='agreement',
            name='users',
            field=models.ManyToManyField(related_name='agreements', through='groups.UserAgreement',
                                         to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='group',
            name='active_agreement',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE,
                                       related_name='active_group', to='groups.Agreement'),
        ),
    ]
