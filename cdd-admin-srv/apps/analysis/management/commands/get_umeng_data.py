from django.core.management.base import BaseCommand

from apps.analysis.umeng import Umeng


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--date', '-d', action='store', dest='date'
        )

    def handle(self, *args, **options):
        print('Sync...')

        umeng = Umeng(options['date'])
        ret = umeng.channel_data()
        print(ret)

        return
