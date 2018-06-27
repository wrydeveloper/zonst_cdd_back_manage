from datetime import datetime, timedelta, date

from django.db import connection, connections

from . import channel
from . import user
from . import proxy
from .models import NumberBetDataDay, SportsBetDataDay, PayDataDay
from utils.sql import namedtuplefetchall


def channel_data_analysis(date_str=None):
    if not date_str:
        date_str = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

    records = {}

    cursor = connection.cursor()

    records = channel.get_cpa_data(cursor, records, date_str)
    records = channel.get_cps_data(cursor, records, date_str)
    records = channel.get_pay_user(cursor, records, date_str)
    records = channel.get_coupon_fee(cursor, records, date_str)
    records = channel.get_charge_money(cursor, records, date_str)
    records = channel.get_cpd_data(records, date_str)
    records = channel.get_cpc_data(cursor, records, date_str)
    records = channel.get_channel_price(cursor, records)
    records = channel.compute_channel_fee(records)
    channel.generate_channel_data(records, date_str)

    return


def proxy_data_analysis(date_str=None):
    if not date_str:
        date_str = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

    records = {}

    cursor = connection.cursor()

    records = proxy.get_proxy_data(cursor, records, date_str)
    records = proxy.get_proxy_price(records)
    records = proxy.compute_proxy_fee(records)
    proxy.generate_proxy_data(records, date_str)

    return


def number_bet_data_analysis(date_str=None):
    if not date_str:
        date_str = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

    cursor = connection.cursor()

    sql = """SELECT SUM(total_money) AS total_money, cdd_lottery.lottery_name, lottery_period 
             FROM cdd_lottery_order_ticket 
             JOIN cdd_lottery ON cdd_lottery_order_ticket.lottery_alias = cdd_lottery.lottery_alias
             WHERE order_date = '{date}' AND ticket_status = '0000'
             GROUP BY cdd_lottery.lottery_name, lottery_period;""".format(date=date_str)
    cursor.execute(sql)
    rows = namedtuplefetchall(cursor)

    obj_list = []
    for row in rows:
        try:
            obj = NumberBetDataDay.objects.get(lottery_type=row.lottery_name, lottery_period=row.lottery_period,
                                               report_date=datetime.strptime(date_str, '%Y-%m-%d'))
            obj.total_money = row.total_money
            obj.save()
        except NumberBetDataDay.DoesNotExist:
            obj = NumberBetDataDay(lottery_type=row.lottery_name, lottery_period=row.lottery_period,
                                   total_money=row.total_money, report_date=datetime.strptime(date_str, '%Y-%m-%d'))
            obj_list.append(obj)

    NumberBetDataDay.objects.bulk_create(obj_list)

    return


def sports_bet_data_analysis(date_str=None):
    if not date_str:
        date_str = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

    cursor = connection.cursor()

    sql = """SELECT SUM(bet_money) AS total_money, game AS lottery_type
             FROM cdd_game_order
             WHERE order_date = '{date}' AND order_status IN (2, 5, 6)
             GROUP BY game""".format(date=date_str)
    cursor.execute(sql)
    rows = namedtuplefetchall(cursor)

    obj_list = []
    for row in rows:
        try:
            obj = SportsBetDataDay.objects.get(lottery_type=row.lottery_type,
                                               report_date=datetime.strptime(date_str, '%Y-%m-%d'))
            obj.total_money = row.total_money
            obj.save()
        except SportsBetDataDay.DoesNotExist:
            obj = SportsBetDataDay(lottery_type=row.lottery_type, total_money=row.total_money,
                                   report_date=datetime.strptime(date_str, '%Y-%m-%d'))
            obj_list.append(obj)

    SportsBetDataDay.objects.bulk_create(obj_list)

    return


def pay_data_analysis(date_str=None):
    if not date_str:
        date_str = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

    cursor = connections['pay'].cursor()

    sql = """SELECT SUM(total_fee) AS total_money, service_config.srv_name, pay_type
             FROM orders
             JOIN service_config ON orders.service_id = service_config.id
             WHERE created_at::date = '{date}' AND status = 'success'
             GROUP BY service_config.srv_name, pay_type""".format(date=date_str)
    cursor.execute(sql)
    rows = namedtuplefetchall(cursor)

    obj_list = []
    for row in rows:
        try:
            obj = PayDataDay.objects.get(pay_type=row.pay_type, srv_name=row.srv_name,
                                         report_date=datetime.strptime(date_str, '%Y-%m-%d'))
            obj.total_money = row.total_money
            obj.save()
        except PayDataDay.DoesNotExist:
            obj = PayDataDay(pay_type=row.pay_type, srv_name=row.srv_name, total_money=row.total_money,
                             report_date=datetime.strptime(date_str, '%Y-%m-%d'))
            obj_list.append(obj)

    PayDataDay.objects.bulk_create(obj_list)

    return


def user_data_analysis(date_str=None):
    if date_str:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    else:
        date_obj = date.today()

    cursor = connection.cursor()

    for n in range(1, 92):
        date_str = (date_obj - timedelta(days=n)).strftime('%Y-%m-%d')

        records = {}

        records = user.get_cpa_data(cursor, records, date_str)
        records = user.get_cps_data(cursor, records, date_str)

        for m in (1, 3, 7, 15, 30, 60, 90):
            day = 'day{delta}'.format(delta=m)
            day_date_str = (date_obj - timedelta(days=m)).strftime('%Y-%m-%d')
            records = user.get_day_data(cursor, records, date_str, day_date_str, day)

        user.generate_user_data(records, date_str)

    return
