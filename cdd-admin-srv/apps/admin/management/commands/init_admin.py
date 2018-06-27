from django.core.management.base import BaseCommand

from apps.admin.models import Admin
from apps.promotion.models import Commerce, Proxy, Channel


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Init...')
        commerce_list = Commerce.objects.all()
        for commerce in commerce_list:
            Admin.objects.create(name=commerce.bd_id, role_id=2)

        proxy_list = Proxy.objects.all()
        for proxy in proxy_list:
            Admin.objects.create(name=proxy.id, role_id=3)

        channel_list = Channel.objects.all()
        for channel in channel_list:
            Admin.objects.create(name=channel.id, role_id=4)
        print('Done.')
        return
