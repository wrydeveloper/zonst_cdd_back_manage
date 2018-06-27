from django.db import models
from django.contrib.postgres.fields import JSONField


class Point(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cdd_point_info'
        ordering = ('-created_at',)


class Event(models.Model):
    id = models.AutoField(primary_key=True)

    point_id = models.IntegerField(default=1)
    channel_id = models.IntegerField(default=100001)
    user_id = models.IntegerField(default=0)
    platform = models.IntegerField(default=1)
    ip = models.CharField(max_length=50)
    ua = models.CharField(max_length=500)
    params = JSONField(default=dict)

    created_at = models.DateTimeField()

    class Meta:
        db_table = 'cdd_event_info'
        ordering = ('-created_at',)
