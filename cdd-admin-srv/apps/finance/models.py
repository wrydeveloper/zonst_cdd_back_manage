from django.db import models


class Recharge(models.Model):

    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    product_name = models.CharField(max_length=100)
    product_desc = models.CharField(max_length=100)
    charge_money = models.IntegerField()
    order_id = models.CharField(max_length=100)
    platform_order_id = models.CharField(max_length=100)
    pay_type = models.IntegerField()
    pay_status = models.IntegerField()
    mark = models.CharField(max_length=100)
    order_time = models.DateTimeField()

    class Meta:
        db_table = 'cdd_wallet_recharge'
        managed = False
        ordering = ('-order_time',)


class Withdraw(models.Model):

    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    cash_money = models.IntegerField()
    order_id = models.CharField(max_length=100)
    status = models.IntegerField()
    status_message = models.CharField(max_length=100)
    status_time = models.DateTimeField()
    mark = models.CharField(max_length=100)
    req_time = models.DateTimeField()

    class Meta:
        db_table = 'cdd_user_wallet_cash'
        managed = False
        ordering = ('-req_time',)


class Bill(models.Model):

    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    balance_before = models.IntegerField()
    balance_now = models.IntegerField()
    fee = models.IntegerField()
    type = models.IntegerField()
    order_id = models.CharField(max_length=100)
    mark = models.CharField(max_length=100)
    add_time = models.DateTimeField()

    class Meta:
        db_table = 'cdd_user_wallet_detail'
        managed = False
        ordering = ('-add_time',)
