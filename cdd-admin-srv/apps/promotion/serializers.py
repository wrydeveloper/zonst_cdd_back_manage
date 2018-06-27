from django.conf import settings

from rest_framework import serializers

from . import models
from apps.admin.models import Admin


class CommerceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Commerce
        fields = '__all__'

    def create(self, validated_data):
        instance = super(CommerceSerializer, self).create(validated_data)

        Admin.objects.create(role_id=2, name=instance.bd_id)

        return instance

    def to_representation(self, instance):
        ret = super(CommerceSerializer, self).to_representation(instance)

        ret.update({
            'add_time': instance.add_time.strftime('%Y-%m-%d %H:%M:%S')
        })

        return ret


class CommerceOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Commerce
        fields = ('id', 'bd_name')


class ProxySerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(required=False, allow_blank=True)
    qq = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = models.Proxy
        exclude = ('password',)

    def create(self, validated_data):
        instance = super(ProxySerializer, self).create(validated_data)
        instance.set_password(settings.DEFAULT_PASSWORD)
        instance.save()

        Admin.objects.create(role_id=3, name=instance.id)

        return instance

    def to_representation(self, instance):
        ret = super(ProxySerializer, self).to_representation(instance)

        try:
            commerce = models.Commerce.objects.get(id=instance.bd_id)
        except models.Commerce.DoesNotExist:
            commerce = None

        ret.update({
            'bd_name': commerce.bd_name if commerce else None,
            'add_time': instance.add_time.strftime('%Y-%m-%d %H:%M:%S')
        })

        return ret


class ProxyOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Proxy
        fields = ('id', 'proxy_name')


class ChannelSerializer(serializers.ModelSerializer):
    proxy_id = serializers.IntegerField(required=False)
    real_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = models.Channel
        exclude = ('password',)

    def create(self, validated_data):
        user = self.context['user']

        if user.role == 'proxy':
            validated_data.update({
                'proxy_id': user.id
            })

        instance = super(ChannelSerializer, self).create(validated_data)
        instance.set_password(settings.DEFAULT_PASSWORD)
        instance.save()

        Admin.objects.create(role_id=4, name=instance.id)

        return instance

    def to_representation(self, instance):
        ret = super(ChannelSerializer, self).to_representation(instance)

        try:
            proxy = models.Proxy.objects.get(id=instance.proxy_id)
        except models.Proxy.DoesNotExist:
            proxy = None

        ret.update({
            'proxy_name': proxy.proxy_name if proxy else None,
            'add_time': instance.add_time.strftime('%Y-%m-%d %H:%M:%S'),
            'promotion_url': settings.PROMOTION_URL.format(channel=instance.id),
            'h5_url': settings.H5_URL.format(channel=instance.id),
            'android_url': settings.ANDROID_URL.format(channel=instance.id),
            'ios_url': settings.IOS_URL.format(channel=instance.id)
        })

        return ret


class ChannelOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Channel
        fields = ('id',)
