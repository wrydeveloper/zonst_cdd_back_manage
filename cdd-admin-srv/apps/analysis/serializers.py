from django.db import connection

from rest_framework import serializers

from utils.sql import namedtuplefetchall

from . import models
from apps.promotion.models import Proxy


class ChannelDataDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ChannelDataDay
        fields = '__all__'


class ProxyDataDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProxyDataDay
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(ProxyDataDaySerializer, self).to_representation(instance)

        try:
            proxy = Proxy.objects.get(id=instance.proxy_id)
        except Proxy.DoesNotExist:
            proxy = None

        ret.update({
            'proxy_name': proxy.proxy_name if proxy else None
        })

        return ret


class UserDataDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserDataDay
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(UserDataDaySerializer, self).to_representation(instance)

        cursor = connection.cursor()
        sql = """SELECT cdd_proxy_info.proxy_name, cdd_bd_info.bd_name
                 FROM cdd_channel_info 
                 JOIN cdd_proxy_info ON cdd_channel_info.proxy_id = cdd_proxy_info.id
                 JOIN cdd_bd_info ON cdd_proxy_info.bd_id = cdd_bd_info.id
                 WHERE cdd_channel_info.id = {channel}""".format(channel=instance.channel_id)
        cursor.execute(sql)
        rows = namedtuplefetchall(cursor)

        ret.update({
            'proxy_name': rows[0].proxy_name,
            'bd_name': rows[0].bd_name,
            'day1': round(instance.day1 / instance.cpa_data * 100, 2) if instance.cpa_data else 0,
            'day3': round(instance.day3 / instance.cpa_data * 100, 2) if instance.cpa_data else 0,
            'day7': round(instance.day7 / instance.cpa_data * 100, 2) if instance.cpa_data else 0,
            'day15': round(instance.day15 / instance.cpa_data * 100, 2) if instance.cpa_data else 0,
            'day30': round(instance.day30 / instance.cpa_data * 100, 2) if instance.cpa_data else 0,
            'day60': round(instance.day60 / instance.cpa_data * 100, 2) if instance.cpa_data else 0,
            'day90': round(instance.day90 / instance.cpa_data * 100, 2) if instance.cpa_data else 0,
            'arpu': round(instance.cps_data / instance.cpa_data / 100, 2) if instance.cpa_data else 0
        })

        return ret


class NumberBetDataDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.NumberBetDataDay
        fields = '__all__'


class SportsBetDataDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SportsBetDataDay
        fields = '__all__'


class PayDataDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PayDataDay
        fields = '__all__'
