from django.db import models


class ChannelDataDay(models.Model):
    """
    # 渠道数据
    """
    id = models.AutoField(primary_key=True)

    # 日期
    report_date = models.DateField()
    # 平台
    platform = models.IntegerField()
    # 渠道
    channel_id = models.IntegerField()

    # 交易金额
    cps_data = models.IntegerField(default=0)
    # 注册量
    cpa_data = models.IntegerField(default=0)
    # 安装量
    cpd_data = models.IntegerField(default=0)
    # IP次数
    cpc_data = models.IntegerField(default=0)
    # 展示次数
    cpm_data = models.IntegerField(default=0)

    # 分成比例
    cps_rate = models.IntegerField(default=0)
    # 注册单价
    cpa_price = models.IntegerField(default=0)
    # 安装单价
    cpd_price = models.IntegerField(default=0)
    # 点击单价
    cpc_price = models.IntegerField(default=0)
    # 展示单价
    cpm_price = models.IntegerField(default=0)

    # 付费人次
    pay_user = models.IntegerField(default=0)
    # 订单个数
    order_count = models.IntegerField(default=0)
    # 渠道成本
    channel_fee = models.IntegerField(default=0)
    # 活动成本
    coupon_fee = models.IntegerField(default=0)
    # 充值金额
    charge_money = models.IntegerField(default=0)

    class Meta:
        db_table = 'cdd_channel_report_day'
        unique_together = (('report_date', 'platform', 'channel_id'),)
        ordering = ('-report_date', '-cps_data')


class ProxyDataDay(models.Model):
    """
    # 代理数据
    """
    id = models.AutoField(primary_key=True)

    # 日期
    report_date = models.DateField()
    # 平台
    platform = models.IntegerField()
    # 代理
    proxy_id = models.IntegerField()

    # 交易金额
    cps_data = models.IntegerField(default=0)
    # 注册量
    cpa_data = models.IntegerField(default=0)
    # 安装量
    cpd_data = models.IntegerField(default=0)
    # IP次数
    cpc_data = models.IntegerField(default=0)
    # 展示次数
    cpm_data = models.IntegerField(default=0)

    # 分成比例
    cps_rate = models.IntegerField(default=0)
    # 注册单价
    cpa_price = models.IntegerField(default=0)
    # 安装单价
    cpd_price = models.IntegerField(default=0)
    # 点击单价
    cpc_price = models.IntegerField(default=0)
    # 展示单价
    cpm_price = models.IntegerField(default=0)

    # 付费人次
    pay_user = models.IntegerField(default=0)
    # 订单个数
    order_count = models.IntegerField(default=0)
    # 渠道成本
    proxy_fee = models.IntegerField(default=0)
    # 活动成本
    coupon_fee = models.IntegerField(default=0)
    # 充值金额
    charge_money = models.IntegerField(default=0)

    class Meta:
        db_table = 'cdd_proxy_report_day'
        unique_together = (('report_date', 'platform', 'proxy_id'),)
        ordering = ('-report_date', '-cps_data')


class NumberBetDataDay(models.Model):
    id = models.AutoField(primary_key=True)

    # 日期
    report_date = models.DateField()
    # 总额
    total_money = models.IntegerField()
    # 彩种
    lottery_type = models.CharField(max_length=100)
    # 期次
    lottery_period = models.CharField(max_length=100)

    class Meta:
        db_table = 'cdd_number_bet_report_day'
        unique_together = (('report_date', 'lottery_type', 'lottery_period'),)
        ordering = ('-report_date',)


class SportsBetDataDay(models.Model):
    id = models.AutoField(primary_key=True)

    # 日期
    report_date = models.DateField()
    # 总额
    total_money = models.IntegerField()
    # 彩种
    lottery_type = models.CharField(max_length=100)

    class Meta:
        db_table = 'cdd_sports_bet_report_day'
        unique_together = (('report_date', 'lottery_type'),)
        ordering = ('-report_date',)


class PayDataDay(models.Model):
    id = models.AutoField(primary_key=True)

    # 日期
    report_date = models.DateField()
    # 总额
    total_money = models.IntegerField()
    # 支付类型
    pay_type = models.CharField(max_length=100)
    # 支付商户
    srv_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'cdd_pay_report_day'
        unique_together = (('report_date', 'pay_type', 'srv_name'),)
        ordering = ('-report_date',)


class UserDataDay(models.Model):
    id = models.AutoField(primary_key=True)

    # 日期
    report_date = models.DateField()
    # 平台
    platform = models.IntegerField()
    # 渠道
    channel_id = models.IntegerField()
    # 代理
    proxy_id = models.IntegerField()
    # 商务
    bd_id = models.IntegerField()
    day1 = models.IntegerField()
    day3 = models.IntegerField()
    day7 = models.IntegerField()
    day15 = models.IntegerField()
    day30 = models.IntegerField()
    day60 = models.IntegerField()
    day90 = models.IntegerField()
    # 交易金额
    cps_data = models.IntegerField()
    # 注册数量
    cpa_data = models.IntegerField()

    class Meta:
        db_table = 'cdd_user_report_day'
        unique_together = (('report_date', 'platform', 'channel_id'),)
        ordering = ('-report_date', '-cps_data')
