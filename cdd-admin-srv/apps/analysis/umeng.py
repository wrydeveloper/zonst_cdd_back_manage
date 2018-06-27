import time
import requests

from django.conf import settings

from apps import errors


class Umeng(object):

    def __init__(self, report_date):
        self.username = settings.UMENG_USERNAME
        self.password = settings.UMENG_PASSWORD
        self.android_key = settings.UMENG_ANDROID_KEY
        self.ios_key = settings.UMENG_IOS_KEY
        self.auth_token = ''
        self.report_date = report_date

        self.login()

    def login(self):
        url = 'http://api.umeng.com/authorize'
        data = {
            'email': self.username,
            'password': self.password
        }
        r = requests.post(url, data)
        data = r.json()

        if data['code'] != 200:
            raise errors.raise_server_error('友盟登录失败！')

        self.auth_token = data['auth_token']

        return

    def channel_data(self):
        android_data_list = self.channel_data_android()
        ios_data_list = self.channel_data_ios()

        return android_data_list + ios_data_list

    def channel_data_android(self):
        ret = []

        page = 1
        while True:
            url = 'http://api.umeng.com/channels'
            params = {
                'auth_token': self.auth_token,
                'appkey': self.android_key,
                'per_page': 50,
                'page': page,
                'date': self.report_date
            }
            r = requests.get(url, params=params, headers={'Connection': 'close'})
            data = r.json()
            if not data:
                break

            for item in data:
                item.update({
                    'platform': 2
                })

            ret.extend(data)
            page += 1

            time.sleep(2)

        return ret

    def channel_data_ios(self):
        ret = []

        page = 1
        while True:
            url = 'http://api.umeng.com/channels'
            params = {
                'auth_token': self.auth_token,
                'appkey': self.ios_key,
                'per_page': 50,
                'page': page,
                'date': self.report_date
            }
            r = requests.get(url, params=params)
            data = r.json()
            if not data:
                break

            for item in data:
                item.update({
                    'platform': 3
                })

            ret.extend(data)
            page += 1

            time.sleep(2)

        return ret
