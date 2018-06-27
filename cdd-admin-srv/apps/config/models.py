from django.db import models


class Lottery(models.Model):
    id = models.AutoField(primary_key=True)
    lottery_name = models.CharField(max_length=100)
    lottery_alias = models.CharField(max_length=100)
    lottery_type = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    status = models.IntegerField(default=0)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cdd_lottery'
        managed = False
        ordering = ('-add_time',)


class PayMerchant(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    pay_type = models.IntegerField(default=0)
    rate = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    contacts = models.CharField(max_length=100, default='')
    appid = models.CharField(max_length=100)
    appkey = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pay_merchant_info'
        managed = False
        ordering = ('-add_time',)


class PayChannel(models.Model):
    id = models.AutoField(primary_key=True)
    channel_name = models.CharField(max_length=100)
    channel_id = models.CharField(max_length=100)

    class Meta:
        db_table = 'pay_channel_info'
        managed = False
        ordering = ('-id',)


class Banner(models.Model):
    id = models.AutoField(primary_key=True)
    banner_theme = models.CharField(max_length=100)
    banner_desc = models.CharField(max_length=100)
    banner_type = models.IntegerField(default=1)
    banner_status = models.IntegerField(default=0)
    img_url = models.CharField(max_length=100)
    target_url = models.CharField(max_length=100)
    target_activity = models.CharField(max_length=100)
    target_args = models.CharField(max_length=100)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cdd_config_banner'
        managed = False
        ordering = ('-add_time',)


# app 引导页
class BootPage(models.Model):
    id = models.AutoField(primary_key=True)
    bootpage_theme = models.CharField(max_length=100)
    bootpage_desc = models.CharField(max_length=100)
    bootpage_type = models.SmallIntegerField(default=1)
    bootpage_status = models.SmallIntegerField(default=0)
    target_url = models.CharField(max_length=100)
    img_url = models.CharField(max_length=100)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cdd_config_bootpage'
        managed = False
        ordering = ('-add_time',)


class Service(models.Model):
    id = models.AutoField(primary_key=True)
    srv_name = models.CharField(max_length=100)
    secret_key = models.CharField(max_length=100)

    class Meta:
        db_table = 'service_config'
        managed = False
