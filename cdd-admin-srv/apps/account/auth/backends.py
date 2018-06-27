import time
import json

from django.contrib.auth.backends import ModelBackend

from utils.cache import cache

from apps.account.models import User
from apps.promotion.models import Proxy, Channel


class CommerceAuthenticationBackend(ModelBackend):

    def authenticate(self, **credentials):
        try:
            username = credentials['username']
            password = credentials['password']
        except KeyError:
            return None

        t = int(time.time())

        salt = User._get_user_salt(login_name=username, t=t)
        if salt is None:
            return None

        user = User._get_user(login_name=username, login_password=password, t=t, salt=salt)
        if user is None:
            return None

        # 缓存用户信息
        cache.hset('user:user', user.user_id, json.dumps(user._raw_objects))

        return user


class ProxyAuthenticationBackend(ModelBackend):

    def authenticate(self, **credentials):
        try:
            username = credentials['username']
            password = credentials['password']
        except KeyError:
            return None

        try:
            proxy = Proxy.objects.get(proxy_name=username)
        except Proxy.DoesNotExist:
            return None

        if not proxy.check_password(password):
            return None

        return proxy


class ChannelAuthenticationBackend(ModelBackend):

    def authenticate(self, **credentials):
        try:
            username = credentials['username']
            password = credentials['password']
        except KeyError:
            return None

        try:
            channel = Channel.objects.get(id=username)
        except (Channel.DoesNotExist, ValueError):
            return None

        if not channel.check_password(password):
            return None

        return channel
