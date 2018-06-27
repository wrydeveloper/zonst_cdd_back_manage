DEBUG = True

# =============
# = Databases =
# =============
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cddclientapp',
        'USER': 'cddclient',
        'PASSWORD': 'digitallife#cddclientapp#123',
        'HOST': '172.17.0.1',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
    },
    'pay': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cddpayapp',
        'USER': 'cddpay',
        'PASSWORD': 'digitallife#cddpayapp#123',
        'HOST': '172.17.0.1',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
    }
}

# ========
# = RABC =
# ========
# rabc网站ID (需管理员分配)
RBAC_SITE_ID = 35
# 关闭验证码
ENABLE_LOGIN_CAPTCHA = False
# rbac密钥 (需管理员分配)
RBAC_SECRET_KEY = 'f8984260-41bb-4773-b357-3deaae998767'

# rbac接口地址(默认)
RBAC_USER_SALT_URL = 'http://rbac.api.xq5.com/auth/salt'
RBAC_USER_DATA_URL = 'http://rbac.api.xq5.com/auth/login'

# =============
# = Promotion =
# =============
H5_URL = 'http://h5-client.wangzheka.cn?c={channel}'
ANDROID_URL = 'http://api-channel-test.duoduocp.cn?c={channel}'
IOS_URL = 'http://api-channel-test.duoduocp.cn?c={channel}'
PROMOTION_URL = 'https://p.duoduocp.cn/lotteryspread/index.html?c={channel}'

# ===========
# = Finance =
# ===========
PAY_URL = 'http://paysrv.wangzheka.cn/v1/cash/pay'
NOTIFY_URL = 'http://clientsrv.wangzheka.cn/v1/client/user/cash_notification'

# ==========
# = Caches =
# ==========
CACHES = {
    'default': 'redis://:digital%23life@172.17.0.1:6379/5',
    'event': 'redis://:digital%23life@172.17.0.1:6379/7',
    'lottery': 'redis://:digital%23life@172.17.0.1:6379/1'
}

# ===========
# = Uploads =
# ===========
IMG_PATH = 'temp/img/'
APK_PATH = 'temp/apk/'
IMG_URL = 'http://dl.wangzheka.cn/img/'
APK_URL = 'http://dl.wangzheka.cn/apk/'

# =========
# = Umeng =
# =========
UMENG_USERNAME = '3457479725@qq.com'
UMENG_PASSWORD = 'digitallife#123'
UMENG_ANDROID_KEY = '5a6fd77ef43e480c740000a8',
UMENG_IOS_KEY = '5a6fd74f8f4a9d7e5a00003d'

DEFAULT_PASSWORD = '123456'
DEFAULT_CHANNEL = 100001
