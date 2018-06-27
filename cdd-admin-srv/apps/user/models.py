from django.db import models


class User(models.Model):
    """
    # 用户表
    """

    id = models.IntegerField(primary_key=True)
    nick_name = models.CharField(max_length=100)
    real_name = models.CharField(max_length=100)
    avatar_url = models.URLField()
    password = models.CharField(max_length=500)
    id_card = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    bank_card = models.CharField(max_length=100)
    bank_addr = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    wx_id = models.CharField(max_length=100)
    channel = models.CharField(max_length=100)
    vip_type = models.IntegerField(default=0)
    reg_ip = models.CharField(max_length=50)
    reg_time = models.DateTimeField()
    status = models.IntegerField(default=0)
    platform = models.IntegerField(default=0)
    last_login_time = models.DateTimeField()
    inviter_id = models.IntegerField()

    class Meta:
        db_table = 'cdd_user'
        managed = False
        ordering = ('-reg_time',)


class UserWallet(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    balance = models.IntegerField()
    balance_freeze = models.IntegerField()

    class Meta:
        db_table = 'cdd_user_wallet'
        managed = False
