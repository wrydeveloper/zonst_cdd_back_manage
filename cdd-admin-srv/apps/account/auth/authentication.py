import jwt
import json

from django.utils.encoding import smart_text
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework_jwt.settings import api_settings

from apps.account.models import User
from apps.promotion.models import Proxy, Channel
from utils.cache import cache

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class BaseJSONWebTokenAuthentication(BaseAuthentication):

    def get_jwt_value(self, request):
        pass

    def authenticate(self, request):
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None

        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            msg = _('Invalid token.')
            raise exceptions.AuthenticationFailed(msg)

        user = self.authenticate_credentials(payload, request)

        return user, jwt_value

    @staticmethod
    def authenticate_credentials(payload, request):
        user_id = payload.get('user_id', '')
        role = payload.get('role', '')

        if '' in (user_id, role):
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)

        if role == 'commerce':
            v = cache.hget('user:user', user_id)
            try:
                obj = json.loads(v)
                user = User.init_from_dict(obj)
            except json.JSONDecodeError:
                return None
        elif role == 'proxy':
            try:
                user = Proxy.objects.get(id=user_id)
            except Proxy.DoesNotExist:
                return None
        else:
            try:
                user = Channel.objects.get(id=user_id)
            except Channel.DoesNotExist:
                return None

        return user


class JSONWebTokenAuthentication(BaseJSONWebTokenAuthentication):

    www_authenticate_realm = 'api'

    def get_jwt_value(self, request):
        auth = get_authorization_header(request).split()
        auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()

        if not auth or smart_text(auth[0].lower()) != auth_header_prefix:
            return None

        if len(auth) == 1:
            msg = _('Invalid Authorization header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]

    def authenticate_header(self, request):
        return '{0} realm="{1}"'.format(api_settings.JWT_AUTH_HEADER_PREFIX, self.www_authenticate_realm)
