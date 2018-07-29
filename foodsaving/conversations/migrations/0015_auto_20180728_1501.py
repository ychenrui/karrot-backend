# Generated by Django 2.0.7 on 2018-07-28 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0014_auto_20180717_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversationparticipant',
            name='notified_up_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='conversationparticipants_notified_up_to', to='conversations.ConversationMessage'),
        ),
        migrations.AddField(
            model_name='conversationthreadparticipant',
            name='notified_up_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='threadparticipants_notified_up_to', to='conversations.ConversationMessage'),
        ),
        migrations.AlterField(
            model_name='conversationparticipant',
            name='seen_up_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='conversationparticipants_seen_up_to', to='conversations.ConversationMessage'),
        ),
        migrations.AlterField(
            model_name='conversationthreadparticipant',
            name='seen_up_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='threadparticipants_seen_up_to', to='conversations.ConversationMessage'),
        ),
    ]
