import os

from django.conf import settings
from django.contrib import auth

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from apps.promotion.models import Channel

from apps import errors

jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ('username', 'password')

    def save(self, **kwargs):
        username = self.validated_data.pop('username')
        password = self.validated_data.pop('password')

        user = auth.authenticate(username=username, password=password)
        if not user or not user.is_authenticated:
            raise errors.raise_server_error('账户或密码错误！')

        level = 'default'
        if user.role == 'commerce':
            payload = {
                'user_id': user.user_id,
                'role': user.role
            }
        elif user.role == 'proxy':
            if user.proxy_level == 1:
                level = 'high'
            payload = {
                'user_id': user.id,
                'role': user.role
            }
        else:
            payload = {
                'user_id': user.id,
                'role': user.role
            }

        data = {
            'token': jwt_encode_handler(payload),
            'role': user.role,
            'level': level
        }

        return data


class ChannelInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        exclude = ('password',)

    def to_representation(self, instance):
        ret = super(ChannelInformationSerializer, self).to_representation(instance)

        ret.update({
            'add_time': instance.add_time.strftime('%Y-%m-%d %H:%M:%S'),
            'promotion_url': settings.PROMOTION_URL.format(channel=instance.id),
            'h5_url': settings.H5_URL.format(channel=instance.id),
            'android_url': settings.ANDROID_URL.format(channel=instance.id),
            'ios_url': settings.IOS_URL.format(channel=instance.id)
        })

        return ret


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=20, write_only=True)
    new_password = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        fields = ('old_password', 'new_password')

    def save(self, user):
        old_password = self.validated_data.pop('old_password')
        new_password = self.validated_data.pop('new_password')

        if not user.check_password(old_password):
            raise errors.raise_server_error('旧密码错误!')

        user.set_password(new_password)
        user.save()

        return
