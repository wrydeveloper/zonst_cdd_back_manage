import json
import time
import requests
from urllib.parse import urlencode

from django.conf import settings

from .auth.utils import hexdigest_password, hexdigest_hash


class User(object):

    @classmethod
    def init_from_dict(cls, d):
        obj = cls()
        for key, value in d.items():
            setattr(obj, key, value)

        setattr(obj, "_raw_objects", d)
        return obj

    @property
    def is_authenticated(self):
        """是否授权用户"""
        return True

    @property
    def is_active(self):
        """是否活动用户"""
        return True

    @property
    def is_anonymous(self):
        """是否匿名用户"""
        return False

    @property
    def role(self):
        return 'commerce'

    @staticmethod
    def _get_user_salt(login_name=None, t=None):
        """获取用户salt"""
        interface_url = settings.RBAC_USER_SALT_URL
        rbac_secret_key = settings.RBAC_SECRET_KEY
        site_id = settings.RBAC_SITE_ID

        sign = hexdigest_hash(secret_key=rbac_secret_key, login_name=login_name, t=t, site_id=site_id)
        request_args = dict(login_name=login_name, t=t, sign=sign, site_id=site_id)
        request_url = "%s?%s" % (interface_url, urlencode(request_args))

        r = None
        for _ in range(3):
            try:
                r = requests.get(request_url, headers={'Connection': 'close'})
            except requests.ConnectionError:
                time.sleep(0.01)
                pass

        if r.status_code == 200:
            rr = json.loads(r.text)
            if rr['status'] == 200:
                return rr['salt']

        return None

    @staticmethod
    def _get_user(login_name=None, login_password=None, t=None, salt=None):
        """获取用户信息"""
        interface_url = settings.RBAC_USER_DATA_URL
        rbac_secret_key = settings.RBAC_SECRET_KEY
        site_id = settings.RBAC_SITE_ID

        password = hexdigest_password("md5", salt, login_password)
        sign = hexdigest_hash(secret_key=rbac_secret_key, login_name=login_name,
                              login_password=password, t=t, site_id=site_id)
        request_args = dict(login_name=login_name, login_password=password, t=t,
                            site_id=site_id, sign=sign)
        request_url = "%s?%s" % (interface_url, urlencode(request_args))

        r = None
        for _ in range(3):
            try:
                r = requests.get(request_url, headers={'Connection': 'close'})
            except requests.ConnectionError:
                time.sleep(0.01)
                pass

        if r.status_code == 200:
            rr = json.loads(r.text)
            if rr['status'] == 200:
                return User.init_from_dict(rr['user'])

        return None

    @staticmethod
    def msg_verify(login_name=None, msg_code=None):
        """获取用户信息"""
        interface_url = settings.RBAC_USER_VERIFY_URL

        request_args = dict(login_name=login_name, msg_code=msg_code)
        request_url = "%s?%s" % (interface_url, urlencode(request_args))
        r = requests.get(request_url)

        if r.status_code == 200:
            rr = json.loads(r.text)
            if rr['status'] == 200:
                return True

        return False
