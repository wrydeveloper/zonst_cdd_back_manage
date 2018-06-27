from django.db import models


class Order(models.Model):

    id = models.IntegerField(primary_key=True)
    out_trade_no = models.CharField(max_length=100)
    service_id = models.IntegerField(default=0)
    pay_type = models.CharField(max_length=100)
    total_fee = models.FloatField()
    mch_create_ip = models.CharField(max_length=100)
    device_info = models.CharField(max_length=100)
    mch_app_name = models.CharField(max_length=100)
    mch_app_id = models.CharField(max_length=100)
    notify_url = models.CharField(max_length=100)
    return_url = models.CharField(max_length=100)
    out_transaction_id = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    pay_channel = models.IntegerField(default=0)
    platform = models.IntegerField(default=1)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'orders'
        managed = False
        ordering = ('-created_at',)


class Refund(models.Model):

    id = models.IntegerField(primary_key=True)
    out_trade_no = models.CharField(max_length=100)
    refund_amount = models.IntegerField(default=0)
    refund_reason = models.CharField(max_length=100)
    out_request_no = models.CharField(max_length=100)
    operator_id = models.CharField(max_length=100)
    return_code = models.CharField(max_length=100)
    trade_no = models.CharField(max_length=100)
    service_id = models.CharField(max_length=100)
    refund_type = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    use_now_pay = models.BooleanField(default=False)

    class Meta:
        db_table = 'refund'
        managed = False
        ordering = ('-id',)
