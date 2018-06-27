import json
from datetime import datetime

from utils.cache import caches

from .models import Event


def insert_to_db(records):
    events = []
    for item in records:
        data = json.loads(item)
        event = Event()
        event.point_id = data['point_id']
        event.channel_id = data['channel_id']
        event.user_id = data['user_id']
        event.platform = data['platform']
        event.ip = data['ip']
        event.ua = data['ua']
        event.params = data['params']
        event.created_at = datetime.strptime(data['created_at'], '%Y-%m-%d %H:%M:%S')

        events.append(event)

    Event.objects.bulk_create(events)

    return


def sync_event_data():
    cache = caches['event']

    key = 'event'

    length = cache.llen(key)
    records = cache.lrange(key, 0, length)
    insert_to_db(records)
    cache.ltrim(key, length, -1)

    return
