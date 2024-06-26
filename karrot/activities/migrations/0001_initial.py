# Generated by Django 1.11.7 on 2017-11-23 12:12

from django.conf import settings
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('places', '0028_extract_activities_app'),
    ]

    state_operations = [
        # These migrations were auto-generated by Django makemigrations.
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('weight', models.FloatField(blank=True, null=True,
                                             validators=[django.core.validators.MinValueValidator(-0.01),
                                                         django.core.validators.MaxValueValidator(10000.0)])),
                ('comment', models.CharField(blank=True, max_length=100000)),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('date', models.DateTimeField()),
                ('description', models.TextField(blank=True)),
                ('max_participants', models.PositiveIntegerField(null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('is_date_changed', models.BooleanField(default=False)),
                ('is_max_participants_changed', models.BooleanField(default=False)),
                ('is_description_changed', models.BooleanField(default=False)),
                ('done_and_processed', models.BooleanField(default=False)),
                ('notifications_sent', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('participants', models.ManyToManyField(related_name='activities', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='ActivitySeries',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('max_participants', models.PositiveIntegerField(blank=True, null=True)),
                ('rule', models.TextField()),
                ('start_date', models.DateTimeField()),
                ('description', models.TextField(blank=True)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='series',
                                            to='places.Place')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='activity',
            name='series',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='activities', to='activities.ActivitySeries'),
        ),
        migrations.AddField(
            model_name='activity',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='activities', to='places.Place'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='about',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.Activity'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='given_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback',
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='feedback',
            unique_together={('about', 'given_by')},
        ),
    ]

    operations = [
        # Only modify Django's state.
        # The database tables are already there - we renamed them earlier.
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
