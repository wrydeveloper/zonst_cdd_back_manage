import copy
from datetime import datetime

from django.conf import settings

from utils.sql import namedtuplefetchall
from .umeng import Umeng

from .models import ChannelDataDay
from apps.promotion.models import Channel

default_data = {
    'channel_fee': 0,
    'coupon_fee': 0,
    'charge_money': 0,
    'cps_data': 0,
    'cpa_data': 0,
    'cpd_data': 0,
    'cpc_data': 0,
    'cpm_data': 0,
    'cps_rate': 0,
    'cpa_price': 0,
    'cpd_price': 0,
    'cpc_price': 0,
    'cpm_price': 0,
    'pay_user': 0,
    'order_count': 0,
    'proxy_type': 0
}


def get_channel_id(channel):
    try:
        channel_id = int(channel)
    except ValueError:
        return settings.DEFAULT_CHANNEL

    if Channel.objects.filter(id=channel_id).exists():
        return channel_id
    return settings.DEFAULT_CHANNEL


def get_cpa_data(cursor, records, date_str):
    # 用户数
    sql = """SELECT COUNT(cdd_user.id) AS user_count, platform, channel, proxy_type
             FROM cdd_user
             JOIN cdd_channel_info ON cdd_user.channel = cdd_channel_info.id
             JOIN cdd_proxy_info ON cdd_channel_info.proxy_id = cdd_proxy_info.id 
             WHERE reg_time::DATE = '{date}' 
             GROUP BY platform, channel, cdd_proxy_info.proxy_type;""".format(date=date_str)
    cursor.execute(sql)
    rows = namedtuplefetchall(cursor)

    for row in rows:
        key = (row.platform, row.channel)
        if key not in records:
            _default = copy.deepcopy(default_data)
            records.setdefault(key, _default)
        records[key]['cpa_data'] = row.user_count
        records[key]['proxy_type'] = row.proxy_type

    return records


def get_cps_data(cursor, records, date_str):
    # 数字彩订单总额
    sql = """SELECT cdd_user.platform, cdd_user.channel, SUM(cdd_lottery_order_ticket.total_money) AS total_money, 
                    proxy_type
             FROM cdd_lottery_order_ticket 
             JOIN cdd_user ON cdd_lottery_order_ticket.user_id = cdd_user.id
             JOIN cdd_channel_info ON cdd_user.channel = cdd_channel_info.id
             JOIN cdd_proxy_info ON cdd_channel_info.proxy_id = cdd_proxy_info.id 
             WHERE cdd_lottery_order_ticket.order_date = '{date}' AND cdd_lottery_order_ticket.ticket_status = '0000'
             GROUP BY cdd_user.platform, cdd_user.channel, proxy_type;""".format(date=date_str)
    cursor.execute(sql)
    rows = namedtuplefetchall(cursor)
    for row in rows:
        key = (row.platform, row.channel)
        if key not in records:
            _default = copy.deepcopy(default_data)
            records.setdefault(key, _default)
        records[key]['cps_data'] = row.total_money
        records[key]['proxy_type'] = row.proxy_type

    # 竞技彩订单总额
    sql = """SELECT cdd_user.platform, cdd_user.channel, SUM(cdd_game_order.bet_money) AS total_money, proxy_type 
             FROM cdd_game_order
             JOIN cdd_user ON cdd_game_order.user_id = cdd_user.id
             JOIN cdd_channel_info ON cdd_user.channel = cdd_channel_info.id
             JOIN cdd_proxy_info ON cdd_channel_info.proxy_id = cdd_proxy_info.id 
             WHERE cdd_game_order.order_date = '{date}' AND cdd_game_order.order_status IN (2, 5, 6)
             GROUP BY cdd_user.platform, cdd_user.channel, proxy_type;""".format(date=date_str)
    cursor.execute(sql)
    rows = namedtuplefetchall(cursor)

    for row in rows:
        key = (row.platform, row.channel)
        if key not in records:
            _default = copy.deepcopy(default_data)
            records.setdefault(key, _default)
        records[key]['cps_data'] += row.total_money
        records[key]['proxy_type'] = row.proxy_type

    return records


def get_order_count(cursor, records, date_str):
    # 数字彩订单数
    sql = """SELECT COUNT(id) AS order_count, cdd_user.platform, cdd_user.channel, proxy_type 
             FROM cdd_lottery_order 
             JOIN cdd_user ON cdd_lottery_order.user_id = cdd_user.id 
             JOIN cdd_channel_info ON cdd_user.channel = cdd_channel_info.id 
             JOIN cdd_proxy_info ON cdd_channel_info.proxy_id = cdd_proxy_info.id 
             WHERE order_date = '{date}' AND order_status IN (2, 5, 6, 7) 
             GROUP BY cdd_user.platform, cdd_user.channel, proxy_type;""".format(date=date_str)
    cursor.execute(sql)
    rows = namedtuplefetchall(cursor)
    for row in rows:
        key = (row.platform, row.channel)
        if key not in records:
            _default = copy.deepcopy(default_data)
            records.setdefault(key, _default)
        records[key]['order_count'] = row.order_count
        records[key]['proxy_type'] = row.proxy_type

    # 竞技彩订单数
    sql = """SELECT COUNT(id) AS order_count, cdd_user.platform, cdd_user.channel, proxy_type 
             FROM cdd_game_order
             JOIN cdd_user ON cdd_game_order.user_id = cdd_user.id
             JOIN cdd_channel_info ON cdd_user.channel = cdd_channel_info.id 
             JOIN cdd_proxy_info ON cdd_channel_info.proxy_id = cdd_proxy_info.id 
             WHERE order_date = '{date}' AND order_status IN (2, 5, 6) 
             GROUP BY cdd_user.platform, cdd_user.channel, proxy_type;""".format(date=date_str)
    cursor.execute(sql)
    rows = namedtuplefetchall(cursor)
    for row in rows:
        key = (row.platform, row.channel)
        if key not in records:
            _default = copy.deepcopy(default_data)
            records.setdefault(key, _default)
        records[key]['order_count'] += row.order_count
        records[key]['proxy_type'] = row.proxy_type

    return records


def get_pay_user(cursor, records, date_str):
    # 数字彩付费人次
    sql = """SELECT COUNT(DISTINCT cdd_lottery_order_ticket.user_id) AS user_count, cdd_user.platform, cdd_user.channel,
                    proxy_type
             FROM cdd_lottery_order_ticket 
             JOIN cdd_user ON cdd_lottery_order_ticket.user_id = cdd_user.id
             JOIN cdd_channel_info ON cdd_user.channel = cdd_channel_info.id
             JOIN cdd_proxy_info ON cdd_channel_info.proxy_id = cdd_proxy_info.id 
             WHERE cdd_lottery_order_ticket.order_date = '{date}' AND cdd_lottery_order_ticket.ticket_status = '0000'
             GROUP BY cdd_user.platform, cdd_user.channel, proxy_type;""".format(date=date_str)
    cursor.execute(sql)
    rows = namedtuplefetchall(cursor)

    for row in rows:
        key = (row.platform, row.channel)
        if key not in records:
            _default = copy.deepcopy(default_data)
            records.setdefault(key, _default)
        records[key]['pay_user'] = row.user_count
        records[key]['proxy_type'] = row.proxy_type

    # 竞技彩付费人次
    sql = """SELECT COUNT(DISTINCT cdd_game_order.user_id) AS user_count, cdd_user.platform, cdd_user.channel,
                    proxy_type
             FROM cdd_game_order 
             JOIN cdd_user ON cdd_game_order.user_id = cdd_user.id
             JOIN cdd_channel_info ON cdd_user.channel = cdd_channel_info.id 
             JOIN cdd_proxy_info ON cdd_channel_info.proxy_id = cdd_proxy_info.id 
             WHERE order_date = '{date}' AND order_status IN (2, 5, 6) 
             GROUP BY cdd_user.platform, cdd_user.channel, proxy_type;""".format(date=date_str)
    cursor.execute(sql)
    rows = namedtuplefetchall(cursor)

    for row in rows:
        key = (row.platform, row.channel)
        if key not in records:
            _default = copy.deepcopy(default_data)
            records.setdefault(key, _default)
        records[key]['pay_user'] += row.user_count
        records[key]['proxy_type'] = row.proxy_type

    return records


def get_coupon_fee(cursor, records, date_str):
    # 活动成本
    sql = """SELECT SUM(face) AS total_money, cdd_user.platform, cdd_user.channel, proxy_type
             FROM cdd_user_coupon JOIN cdd_user ON cdd_user_coupon.user_id = cdd_user.id
             JOIN cdd_channel_info ON cdd_user.channel = cdd_channel_info.id
             JOIN cdd_proxy_info ON cdd_channel_info.proxy_id = cdd_proxy_info.id 
             WHERE used_date = '{date}' AND coupon_status = 1
             GROUP BY cdd_user.platform, cdd_user.channel, proxy_type;""".format(date=date_str)
    cursor.execute(sql)
    rows = namedtuplefetchall(cursor)

    for row in rows:
        key = (row.platform, row.channel)
        if key not in records:
            _default = copy.deepcopy(default_data)
            records.setdefault(key, _default)
        records[key]['coupon_fee'] = row.total_money
        records[key]['proxy_type'] = row.proxy_type

    return records


def get_charge_money(cursor, records, date_str):
    # 充值总额
    sql = """SELECT SUM(charge_money) AS total_money, cdd_user.platform, cdd_user.channel, proxy_type
             FROM cdd_wallet_recharge 
             JOIN cdd_user ON cdd_wallet_recharge.user_id = cdd_user.id
             JOIN cdd_channel_info ON cdd_user.channel = cdd_channel_info.id
             JOIN cdd_proxy_info ON cdd_channel_info.proxy_id = cdd_proxy_info.id 
             WHERE order_time::DATE = '{date}' AND pay_status = 1
             GROUP BY cdd_user.platform, cdd_user.channel, proxy_type;""".format(date=date_str)
    cursor.execute(sql)
    rows = namedtuplefetchall(cursor)

    for row in rows:
        key = (row.platform, row.channel)
        if key not in records:
            _default = copy.deepcopy(default_data)
            records.setdefault(key, _default)
        records[key]['charge_money'] = row.total_money
        records[key]['proxy_type'] = row.proxy_type

    return records


def get_cpd_data(records, date_str):
    # 同步友盟渠道数据
    umeng = Umeng(date_str)
    data = umeng.channel_data()
    for item in data:
        channel = get_channel_id(item['channel'])

        key = (item['platform'], channel)
        if key not in records:
            _default = copy.deepcopy(default_data)
            records.setdefault(key, _default)
        records[key]['cpd_data'] = item['install']

    return records


def get_cpc_data(cursor, records, date_str):
    sql = """SELECT COUNT(1) AS cpc_data, cdd_event_info.platform, cdd_event_info.channel_id, proxy_type
             FROM cdd_event_info
             JOIN cdd_channel_info ON cdd_event_info.channel_id = cdd_channel_info.id
             JOIN cdd_proxy_info ON cdd_channel_info.proxy_id = cdd_proxy_info.id
             WHERE cdd_event_info.created_at::DATE = '{date}' AND cdd_event_info.id = 1
             GROUP BY cdd_event_info.platform, cdd_event_info.channel_id, proxy_type;""".format(date=date_str)
    cursor.execute(sql)
    rows = namedtuplefetchall(cursor)

    for row in rows:
        key = (row.platform, row.channel_id)
        if key not in records:
            _default = copy.deepcopy(default_data)
            records.setdefault(key, _default)
        records[key]['cpc_data'] = row.cpc_data
        records[key]['proxy_type'] = row.proxy_type

    return records


def get_channel_price(cursor, records):
    # 获取渠道价格
    for key, record in records.items():
        sql = """SELECT cdd_channel_info.commission AS channel_commission,  
                        cdd_proxy_info.commission AS proxy_commission, 
                        cdd_proxy_info.proxy_type
                 FROM cdd_channel_info 
                 JOIN cdd_proxy_info ON cdd_channel_info.proxy_id = cdd_proxy_info.id
                 WHERE cdd_channel_info.id = {channel_id}""".format(channel_id=key[1])
        cursor.execute(sql)
        rows = namedtuplefetchall(cursor)
        if not rows:
            continue

        if rows[0].proxy_type == 1:
            record['cps_rate'] = rows[0].channel_commission
        elif rows[0].proxy_type == 2:
            record['cpa_price'] = rows[0].proxy_commission
        elif rows[0].proxy_type == 3:
            record['cpd_price'] = rows[0].proxy_commission
        elif rows[0].proxy_type == 4:
            record['cpc_price'] = rows[0].proxy_commission
        elif rows[0].proxy_type == 5:
            record['cpm_price'] = rows[0].proxy_commission

        record['proxy_type'] = rows[0].proxy_type

    return records


def compute_channel_fee(records):
    # 计算渠道成本
    for key, record in records.items():
        if record['proxy_type'] == 1:
            channel_fee = record['cps_data'] * record['cps_rate'] // 100
        elif record['proxy_type'] == 2:
            channel_fee = record['cpa_data'] * record['cpa_price']
        elif record['proxy_type'] == 3:
            channel_fee = record['cpd_data'] * record['cpd_price']
        elif record['proxy_type'] == 4:
            channel_fee = record['cpc_data'] * record['cpc_price']
        elif record['proxy_type'] == 5:
            channel_fee = record['cpm_data'] * record['cpm_price']
        else:
            channel_fee = 0

        record['channel_fee'] = channel_fee

    return records


def generate_channel_data(records, date_str):
    # 生成渠道数据
    for key, record in records.items():
        try:
            obj = ChannelDataDay.objects.get(channel_id=key[1], platform=key[0],
                                             report_date=datetime.strptime(date_str, '%Y-%m-%d'))
            obj.channel_fee = record['channel_fee']
            obj.coupon_fee = record['coupon_fee']
            obj.charge_money = record['charge_money']
            obj.cps_data = record['cps_data']
            obj.cpa_data = record['cpa_data']
            obj.cpd_data = record['cpd_data']
            obj.cpc_data = record['cpc_data']
            obj.cpm_data = record['cpm_data']
            obj.cps_rate = record['cps_rate']
            obj.cpa_price = record['cpa_price']
            obj.cpd_price = record['cpd_price']
            obj.cpc_price = record['cpc_price']
            obj.cpm_price = record['cpm_price']
            obj.pay_user = record['pay_user']
            obj.order_count = record['order_count']
            obj.save()
        except ChannelDataDay.DoesNotExist:
            ChannelDataDay.objects.create(channel_id=key[1], platform=key[0], channel_fee=record['channel_fee'],
                                          coupon_fee=record['coupon_fee'], charge_money=record['charge_money'],
                                          cps_data=record['cps_data'], cpa_data=record['cpa_data'],
                                          cpd_data=record['cpd_data'], cpc_data=record['cpc_data'],
                                          cpm_data=record['cpm_data'], cps_rate=record['cps_rate'],
                                          cpa_price=record['cpa_price'], cpd_price=record['cpd_price'],
                                          cpc_price=record['cpc_price'], cpm_price=record['cpm_price'],
                                          pay_user=record['pay_user'], order_count=record['order_count'],
                                          report_date=datetime.strptime(date_str, '%Y-%m-%d'))

    return
