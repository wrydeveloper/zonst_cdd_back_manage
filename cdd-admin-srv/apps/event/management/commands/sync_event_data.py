from django.core.management.base import BaseCommand

from apps.event import jobs


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Sync...')
        jobs.sync_event_data()
        print('Done.')
        return
