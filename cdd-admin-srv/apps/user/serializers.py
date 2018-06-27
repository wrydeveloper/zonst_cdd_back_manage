from django.db import connection
from django.db.models import Sum

from rest_framework import serializers

from utils.sql import namedtuplefetchall

from .models import User, UserWallet


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password',)

    def to_representation(self, instance):
        ret = super(UserSerializer, self).to_representation(instance)

        cursor = connection.cursor()
        sql = """SELECT cdd_proxy_info.proxy_name, cdd_bd_info.bd_name
                 FROM cdd_channel_info 
                 JOIN cdd_proxy_info ON cdd_channel_info.proxy_id = cdd_proxy_info.id
                 JOIN cdd_bd_info ON cdd_proxy_info.bd_id = cdd_bd_info.id
                 WHERE cdd_channel_info.id = {channel}""".format(channel=instance.channel)
        cursor.execute(sql)
        rows = namedtuplefetchall(cursor)

        user = self.context['user']
        if user.role == 'channel':
            ret.update({
                'nick_name': ''.join([instance.phone_number[0:3], '****', instance.phone_number[7:]]),
                'phone_number': ''.join([instance.phone_number[0:3], '****', instance.phone_number[7:]])
            })

        invite_count = User.objects.filter(inviter_id=instance.id).count()
        statistic = UserWallet.objects.filter(user_id=instance.id).aggregate(balance=Sum('balance'),
                                                                             balance_freeze=Sum('balance_freeze'))

        ret.update({
            'balance': statistic.get('balance'),
            'balance_freeze': statistic.get('balance_freeze'),
            'invite_count': invite_count,
            'proxy_name': rows[0].proxy_name if rows else '',
            'bd_name': rows[0].bd_name if rows else '',
            'reg_time': instance.reg_time.strftime('%Y-%m-%d %H:%M:%S'),
            'last_login_time': instance.last_login_time.strftime('%Y-%m-%d %H:%M:%S')
        })

        return ret
