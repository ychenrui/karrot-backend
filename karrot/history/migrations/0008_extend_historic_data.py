# Generated by Django 2.2.2 on 2019-06-18 14:25
from collections import defaultdict
from datetime import timedelta

from django.db import migrations
from django.utils.dateparse import parse_datetime
from django_enumfield import enum
from rest_framework import serializers

from karrot.activities.serializers import DateTimeRangeField


class HistoryTypus(enum.Enum):
    GROUP_CREATE = 0
    GROUP_MODIFY = 1
    GROUP_JOIN = 2
    GROUP_LEAVE = 3
    STORE_CREATE = 4
    STORE_MODIFY = 5
    STORE_DELETE = 6
    ACTIVITY_CREATE = 7
    ACTIVITY_MODIFY = 8
    ACTIVITY_DELETE = 9
    SERIES_CREATE = 10
    SERIES_MODIFY = 11
    SERIES_DELETE = 12
    ACTIVITY_DONE = 13
    ACTIVITY_JOIN = 14
    ACTIVITY_LEAVE = 15
    ACTIVITY_MISSED = 16
    APPLICATION_DECLINED = 17
    MEMBER_BECAME_EDITOR = 18
    ACTIVITY_DISABLE = 19
    ACTIVITY_ENABLE = 20
    GROUP_LEAVE_INACTIVE = 21
    GROUP_CHANGE_PHOTO = 22
    GROUP_DELETE_PHOTO = 23
    MEMBER_REMOVED = 24


BATCH_SIZE = 1000


def migrate(apps, schema_editor):
    History = apps.get_model('history', 'History')
    Activity = apps.get_model('activities', 'Activity')

    save_activity_id = []

    # set foreign key to activity
    history_to_update = []
    for h in History.objects.filter(typus__in=(
            HistoryTypus.ACTIVITY_JOIN,
            HistoryTypus.ACTIVITY_LEAVE,
            HistoryTypus.ACTIVITY_DONE,
            HistoryTypus.ACTIVITY_MISSED,
    )):
        if not h.payload:
            continue
        activity_id = h.payload.get('id') or h.payload.get('activity_date')
        if not activity_id:
            continue

        h.activity_id = activity_id
        history_to_update.append(h)

    requested_activity_ids = {h.activity_id for h in history_to_update}
    valid_activity_ids = Activity.objects.filter(id__in=requested_activity_ids).values_list(flat=True)

    for h in history_to_update:
        if h.activity_id in valid_activity_ids:
            save_activity_id.append(h)

    History.objects.bulk_update(save_activity_id, fields=['activity_id'], batch_size=BATCH_SIZE)

    # rewrite old activity payload to default duration
    save_payload = []
    for h in History.objects.filter(typus__in=(
            HistoryTypus.ACTIVITY_JOIN,
            HistoryTypus.ACTIVITY_LEAVE,
    ), payload__date__0__isnull=True):
        if h.payload and 'date' in h.payload:
            date = parse_datetime(h.payload['date'])
            h.payload['date'] = [d.isoformat() for d in [date, date + timedelta(minutes=30)]]
            save_payload.append(h)

    # always use activity serializer for payload
    activity_to_history = defaultdict(list)

    for h in History.objects.filter(typus__in=(
            HistoryTypus.ACTIVITY_DONE,
            HistoryTypus.ACTIVITY_MISSED,
    )).select_related('activity').prefetch_related('activity__activityparticipant_set'):
        if not h.activity_id:
            continue
        activity_to_history[h.activity].append(h)

    class ActivitySerializer(serializers.ModelSerializer):
        class Meta:
            model = Activity
            fields = [
                'id',
                'date',
                'series',
                'place',
                'max_participants',
                'participants',
                'description',
                'is_disabled',
            ]

        participants = serializers.SerializerMethodField()

        date = DateTimeRangeField()

        def get_participants(self, activity):
            return [c.user_id for c in activity.activityparticipant_set.all()]

    for activity, history_list in activity_to_history.items():
        activity_data = ActivitySerializer(activity).data
        for h in history_list:
            h.payload = activity_data
            save_payload.append(h)

    History.objects.bulk_update(save_payload, fields=['payload'], batch_size=BATCH_SIZE)


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0007_auto_20190123_1628'),
    ]

    operations = [migrations.RunPython(migrate, migrations.RunPython.noop, elidable=True)]
