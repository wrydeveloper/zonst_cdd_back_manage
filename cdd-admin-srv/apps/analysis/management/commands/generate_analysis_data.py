from django.core.management.base import BaseCommand

from apps.analysis import jobs


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--date', '-d', action='store', dest='date'
        )

    def handle(self, *args, **options):
        print('Generating...')
        jobs.channel_data_analysis(options['date'])
        jobs.number_bet_data_analysis(options['date'])
        jobs.sports_bet_data_analysis(options['date'])
        jobs.pay_data_analysis(options['date'])
        jobs.user_data_analysis(options['date'])
        jobs.proxy_data_analysis(options['date'])
        print('Done.')
        return
