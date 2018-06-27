import requests

from django.core.management.base import BaseCommand

from apps.finance.models import Withdraw
from apps.user.models import User
from apps.config.models import Service
from utils.md5 import encrypt

class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Generating...')

        try:
            instance = Withdraw.objects.get(id=4)
        except Withdraw.DoesNotExist:
            return

        try:
            user = User.objects.get(id=instance.user_id)
        except User.DoesNotExist:
            return

        try:
            service = Service.objects.get(id=1)
        except Service.DoesNotExist:
            return

        url = 'http://paysrv.duoduocp.cn/v1/cash/pay'
        data = {
            'acc_type': '02',
            'payee_name': user.real_name,
            'payee_card_no': user.bank_card,
            'agent_pay_memo': '提现代付',
            'notify_url': 'http://paysrv.duoduocp.cn/v1/client/user/cash_notification',
            'order_number': instance.order_id,
            'order_amt': instance.cash_money,
            'bank_name': user.bank_name,
            'service_id': 1
        }

        sign = encrypt(data, service.secret_key)
        print('sign', sign)
        data.update({
            'sign': sign
        })
        print(data)

        try:
            r = requests.post(url, data=data)
        except requests.ConnectionError:
            return

        if r.status_code != 200:
            return

        ret = r.json()
        print(ret)

        print('Done.')
        return
