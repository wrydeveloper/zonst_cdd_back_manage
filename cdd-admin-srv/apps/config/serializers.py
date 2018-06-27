from django.db import transaction

from rest_framework import serializers

from utils.cache import caches

from . import models


class LotterySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lottery
        fields = '__all__'

    def update(self, instance, validated_data):
        instance = super(LotterySerializer, self).update(instance, validated_data)

        # 刷新redis
        cache = caches['lottery']
        key = 'lottery:lottery'
        cache.delete(key)

        return instance

    def to_representation(self, instance):
        ret = super(LotterySerializer, self).to_representation(instance)

        ret.update({
            'add_time': instance.add_time.strftime('%Y-%m-%d %H:%M:%S')
        })

        return ret


class PayMerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PayMerchant
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(PayMerchantSerializer, self).to_representation(instance)

        ret.update({
            'add_time': instance.add_time.strftime('%Y-%m-%d %H:%M:%S')
        })

        return ret


class PayChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PayChannel
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    target_args = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    target_activity = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = models.Banner
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(BannerSerializer, self).to_representation(instance)

        ret.update({
            'add_time': instance.add_time.strftime('%Y-%m-%d %H:%M:%S')
        })

        return ret


class BootPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BootPage
        fields = '__all__'

    def create(self, validated_data):
        with transaction.atomic():
            instance = super(BootPageSerializer, self).create(validated_data)
            if validated_data["bootpage_status"] == 1:
                models.BootPage.objects.exclude(id=instance.id).update(bootpage_status=0)
            return instance

    def update(self, instance, validated_data):
        with transaction.atomic():
            models.BootPage.objects.filter(id=instance.id).update(**validated_data)
            if validated_data["bootpage_status"] == 1:
                models.BootPage.objects.exclude(id=instance.id).update(bootpage_status=0)
        return instance


    def to_representation(self, instance):
        ret = super(BootPageSerializer, self).to_representation(instance)

        ret.update({
            'add_time': instance.add_time.strftime('%Y-%m-%d %H:%M:%S')
        })

        return ret
