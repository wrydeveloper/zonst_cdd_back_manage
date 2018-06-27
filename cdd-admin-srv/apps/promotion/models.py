from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager


class Commerce(models.Model):
    id = models.AutoField(primary_key=True)
    bd_name = models.CharField(max_length=100)
    bd_id = models.CharField(max_length=20)
    status = models.IntegerField(default=1)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cdd_bd_info'
        ordering = ('-add_time',)


class Proxy(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    proxy_name = models.CharField(max_length=100, default='')
    company_name = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=20, default='')
    qq = models.CharField(max_length=20, default='')
    bd_id = models.IntegerField(default=0)
    proxy_level = models.IntegerField(default=0)
    proxy_type = models.IntegerField(default=0)
    commission = models.IntegerField(default=0)
    pay_type = models.IntegerField(default=1)
    real_name = models.CharField(max_length=100, default='')
    # 开户姓名
    bank_account = models.CharField(max_length=100, default='')
    bank_name = models.CharField(max_length=100, default='')
    bank_number = models.CharField(max_length=100, default='')
    bank_addr = models.CharField(max_length=100, default='')
    status = models.IntegerField(default=1)
    add_time = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'id'
    objects = UserManager()

    class Meta:
        db_table = 'cdd_proxy_info'
        ordering = ('-add_time',)

    @property
    def role(self):
        return 'proxy'


class Channel(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    real_name = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=20, default='')
    proxy_id = models.IntegerField()
    commission = models.IntegerField(default=0)
    is_used = models.IntegerField(default=0)
    status = models.IntegerField(default=1)
    mark = models.CharField(max_length=255, default='')
    add_time = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'id'
    objects = UserManager()

    class Meta:
        db_table = 'cdd_channel_info'
        ordering = ('-add_time',)

    @property
    def role(self):
        return 'channel'
