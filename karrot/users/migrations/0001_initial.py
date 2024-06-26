# Generated by Django 1.9.7 on 2016-07-21 14:47

from django.db import migrations, models
import django.utils.timezone
import django_enumfield.db.fields
from django_enumfield import enum
import karrot.users.models


# removed code, moved here for compatibility
# can be removed when migration get squashed
class ProfileVisibility(enum.Enum):
    PRIVATE = 0
    CONNECTED_USERS = 1
    COMMUNITIES = 2
    REGISTERED_USERS = 3
    PUBLIC = 4


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('display_name', models.TextField()),
                ('first_name', models.TextField(null=True)),
                ('last_name', models.TextField(null=True)),
                ('profile_visibility', django_enumfield.db.fields.EnumField(default=0, enum=ProfileVisibility)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', karrot.users.models.UserManager()),
            ],
        ),
    ]
