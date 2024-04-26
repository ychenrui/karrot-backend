

import django.contrib.postgres.fields.citext
from django.db import migrations
import karrot.users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0029_change_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=django.contrib.postgres.fields.citext.CICharField(max_length=255, unique=True),
        ),
    ]