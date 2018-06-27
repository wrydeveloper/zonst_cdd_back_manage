from django.db import models
from django.contrib.postgres.fields import JSONField


class OrderNumber(models.Model):

    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    lottery_alias = models.CharField(max_length=100)
    lottery_period = models.CharField(max_length=100)
    tickets = JSONField()
    amount = models.IntegerField(default=1)
    total_money = models.IntegerField(default=0)
    bonus_money = models.IntegerField(default=0)
    coupon_money = models.IntegerField(default=0)
    order_id = models.CharField(max_length=100)
    order_status = models.IntegerField(default=0)
    show_status = models.IntegerField(default=1)
    mark = models.CharField(max_length=100)
    is_followed_order = models.IntegerField(default=0)
    followed_order_id = models.CharField(max_length=100)
    order_date = models.DateField()
    order_time = models.DateTimeField()

    class Meta:
        db_table = 'cdd_lottery_order'
        managed = False
        ordering = ('-order_time',)


class OrderNumberFollow(models.Model):

    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    lottery_alias = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100)
    tickets = JSONField()
    amount = models.IntegerField(default=1)
    total_money = models.IntegerField(default=0)
    mark = models.CharField(max_length=100)
    follow_num = models.IntegerField(default=0)
    follow_remain_num = models.IntegerField(default=0)
    follow_status = models.IntegerField(default=1)
    order_status = models.IntegerField(default=0)
    order_date = models.DateField()
    order_time = models.DateTimeField()

    class Meta:
        db_table = 'cdd_lottery_order_follow'
        managed = False
        ordering = ('-order_time',)


class OrderNumberTicket(models.Model):

    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    lottery_alias = models.CharField(max_length=100)
    lottery_period = models.CharField(max_length=100)
    ante_code = models.CharField(max_length=100)
    amount = models.IntegerField(default=1)
    play_type = models.CharField(max_length=100)
    total_money = models.IntegerField()
    bonus_money = models.IntegerField()
    order_id = models.CharField(max_length=100)
    parent_order_id = models.CharField(max_length=100)
    ticket_index = models.IntegerField()
    ticket_id = models.CharField(max_length=100)
    ticket_serial = models.CharField(max_length=100)
    ticket_dealtime = models.CharField(max_length=100)
    ticket_status = models.CharField(max_length=100)
    ticket_message = models.CharField(max_length=100)
    order_status = models.IntegerField(default=0)
    mark = models.CharField(max_length=100)
    order_date = models.DateField()
    order_time = models.DateTimeField()

    class Meta:
        db_table = 'cdd_lottery_order_ticket'
        managed = False
        ordering = ('-order_time',)


class OrderSports(models.Model):

    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    order_id = models.CharField(max_length=100)
    game = models.CharField(max_length=100)
    lottery_id = models.CharField(max_length=100)
    bet_type = models.CharField(max_length=100)
    bet_multi = models.IntegerField(default=0)
    bet_money = models.IntegerField(default=0)
    coupon_id = models.IntegerField(default=0)
    coupon_money = models.IntegerField(default=0)
    bonus_money = models.IntegerField(default=0)
    bet_codes = models.CharField(max_length=100)
    scheme_id = models.CharField(max_length=100)
    scheme_status = models.IntegerField(default=0)
    code_rate =  models.CharField(max_length=100)
    success_time = models.CharField(max_length=100)
    real_ticketno = models.CharField(max_length=100)
    error_code = models.CharField(max_length=100)
    error_msg = models.CharField(max_length=100)
    order_status = models.IntegerField(default=0)
    order_date = models.DateField()
    order_time = models.DateTimeField()

    class Meta:
        db_table = 'cdd_game_order'
        managed = False
        ordering = ('-order_time',)


class OrderSportsDetail(models.Model):

    id = models.IntegerField(primary_key=True)
    order_id = models.CharField(max_length=100)
    game = models.CharField(max_length=100)
    match_number = models.CharField(max_length=100)
    lottery_id = models.CharField(max_length=100)
    league = models.CharField(max_length=100)
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    ft01_result = models.CharField(max_length=100)
    ft02_result = models.CharField(max_length=100)
    ft03_result = models.CharField(max_length=100)
    ft04_result = models.CharField(max_length=100)
    ft05_result = models.CharField(max_length=100)
    bt01_result = models.CharField(max_length=100)
    bt02_result = models.CharField(max_length=100)
    bt03_result = models.CharField(max_length=100)
    bt04_result = models.CharField(max_length=100)
    is_finished = models.IntegerField(default=0)
    is_normal = models.IntegerField(default=0)
    ft_let_point_multi = models.IntegerField(default=0)
    bt_let_point_multi = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'cdd_game_order_detail'
        managed = False
        ordering = ('id',)
