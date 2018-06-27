import redis

from django.conf import settings


class Cache(object):

    def __init__(self):
        self.clients = {}
        self.init()

    def init(self):
        for alias, url in settings.CACHES.items():
            client = redis.StrictRedis.from_url(url, decode_components=True)
            self.clients[alias] = client

    def __getitem__(self, alias):
        conn = self.clients[alias]

        return conn


caches = Cache()


class DefaultCache(object):

    def __getattr__(self, item):
        return getattr(caches['default'], item)


cache = DefaultCache()
