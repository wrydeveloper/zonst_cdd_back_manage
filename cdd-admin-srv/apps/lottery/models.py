from django.db import models


class NumberPeriodThirdparty(models.Model):

    id = models.IntegerField(primary_key=True)
    lottery_name = models.CharField(max_length=100)
    lottery_alias = models.CharField(max_length=100)
    lottery_period = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    stop_time = models.DateTimeField()
    official_start_time = models.DateTimeField()
    official_stop_time = models.DateTimeField()
    status = models.IntegerField(default=0)
    weekday = models.CharField(max_length=100)
    bonus_code = models.CharField(max_length=100)
    sales_money = models.IntegerField(default=-1)
    bonus_money = models.IntegerField(default=-1)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cdd_lottery_period'
        managed = False
        ordering = ('-add_time',)


class NumberPeriodLocal(models.Model):

    id = models.IntegerField(primary_key=True)
    lottery_alias = models.CharField(max_length=100)
    lottery_period = models.CharField(max_length=100)
    weekday = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    stop_time = models.DateTimeField()
    status = models.IntegerField(default=0)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cdd_lottery_period_local'
        managed = False
        ordering = ('-add_time',)


class NumberLotteryBonus(models.Model):

    id = models.IntegerField(primary_key=True)
    lottery_alias = models.CharField(max_length=100)
    lottery_period = models.CharField(max_length=100)
    play_type = models.CharField(max_length=100)
    is_bomb_bonus = models.IntegerField(default=0)
    ticket_id = models.CharField(max_length=100)
    per_money = models.IntegerField(default=0)
    bonus_money = models.IntegerField(default=0)
    size = models.IntegerField(default=0)
    bonus_level = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    add_date = models.DateField()
    add_time = models.DateTimeField()

    class Meta:
        db_table = 'cdd_lottery_bonus'
        managed = False
        ordering = ('-add_time',)


class SportsLotteryMatch(models.Model):

    id = models.IntegerField(primary_key=True)
    game = models.CharField(max_length=100)
    team_name = models.CharField(max_length=100)
    league = models.CharField(max_length=100)
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    match_color = models.CharField(max_length=100)
    match_number = models.CharField(max_length=100)
    match_date = models.DateField()
    match_weekday = models.IntegerField(default=0)
    match_index = models.CharField(max_length=100)
    unsupport_multi = models.CharField(max_length=100)
    match_status = models.IntegerField(default=0)
    is_normal = models.IntegerField(default=1)
    ft_let_point_multi = models.IntegerField(default=0)
    ft_half_home_point = models.IntegerField(default=0)
    ft_half_away_point = models.IntegerField(default=0)
    ft_home_point = models.IntegerField(default=0)
    ft_away_point = models.IntegerField(default=0)
    bt_let_point_multi = models.DecimalField(max_digits=8, decimal_places=2)
    bt_base_point_multi = models.DecimalField(max_digits=8, decimal_places=2)
    bt_home_point = models.IntegerField(default=0)
    bt_away_point = models.IntegerField(default=0)
    match_time = models.DateTimeField()
    end_time = models.DateTimeField()
    add_time = models.DateTimeField()

    class Meta:
        db_table = 'cdd_game_match'
        managed = False
        ordering = ('-add_time',)

class SportsLotteryBonus(models.Model):

    id = models.IntegerField(primary_key=True)
    game = models.CharField(max_length=100)
    match_number = models.CharField(max_length=100)
    scheme_id = models.CharField(max_length=100)
    is_big_award =  models.IntegerField(default=0)
    level_money = models.IntegerField(default=0)
    win_money = models.IntegerField(default=0)
    prize_times = models.IntegerField(default=0)
    bonus_money = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    bonus_date = models.DateField()

    class Meta:
        db_table = 'cdd_game_bonus'
        managed = False
        ordering = ('-bonus_date',)
