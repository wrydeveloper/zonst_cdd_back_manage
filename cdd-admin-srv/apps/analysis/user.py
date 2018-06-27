import copy
from datetime import datetime

from utils.sql import namedtuplefetchall

from .models import UserDataDay

default_data = {
    'proxy_id': '',
    'bd_id': '',
    'day1': 0,
    'day3': 0,
    'day7': 0,
    'day15': 0,
    'day30': 0,
    'day60': 0,
    'day90': 0,
    'cps_data': 0,
    'cpa_data': 0
}


def get_cpa_data(cursor, records, date_str):
    # CPA
    sql = """SELECT COUNT(cdd_user.id) AS cpa_data, platform, channel, cdd_proxy_info.id AS proxy_id, cdd_bd_info.id AS 
                    bd_id
             FROM cdd_user
             JOIN cdd_channel_info ON cdd_user.channel = cdd_channel_info.id
             JOIN cdd_proxy_info ON cdd_channel_info.proxy_id = cdd_proxy_info.id
             JOIN cdd_bd_info ON cdd_proxy_info.bd_id = cdd_bd_info.id
             WHERE reg_time::DATE = '{date}' 
             GROUP BY platform, channel, cdd_proxy_info.id, cdd_bd_info.id;""".format(date=date_str)
    cursor.execute(sql)
    rows = namedtuplefetchall(cursor)

    for row in rows:
        key = (row.platform, row.channel)
        if key not in records:
            _default = copy.deepcopy(default_data)
            records.setdefault(key, _default)
        records[key]['cpa_data'] = row.cpa_data
        records[key]['proxy_id'] = row.proxy_id
        records[key]['bd_id'] = row.bd_id

    return records


def get_cps_data(cursor, records, date_str):
    # CPS
    sql = """SELECT SUM(cdd_lottery_order_ticket.total_money) AS cps_data, cdd_user.platform, cdd_user.channel,
                    cdd_proxy_info.id AS proxy_id, cdd_bd_info.id AS bd_id
             FROM cdd_lottery_order_ticket 
             JOIN cdd_user ON cdd_lottery_order_ticket.user_id = cdd_user.id
             JOIN cdd_channel_info ON cdd_user.channel = cdd_channel_info.id
             JOIN cdd_proxy_info ON cdd_channel_info.proxy_id = cdd_proxy_info.id
             JOIN cdd_bd_info ON cdd_proxy_info.bd_id = cdd_bd_info.id
             WHERE cdd_lottery_order_ticket.order_date = '{date}' AND cdd_lottery_order_ticket.ticket_status = '0000'
                   AND cdd_user.id IN (SELECT id FROM cdd_user WHERE reg_time::DATE = '{date}')
             GROUP BY cdd_user.platform, cdd_user.channel, cdd_proxy_info.id, cdd_bd_info.id;""".format(date=date_str)
    cursor.execute(sql)
    rows = namedtuplefetchall(cursor)

    for row in rows:
        key = (row.platform, row.channel)
        if key not in records:
            _default = copy.deepcopy(default_data)
            records.setdefault(key, _default)
        records[key]['cps_data'] = row.cps_data
        records[key]['proxy_id'] = row.proxy_id
        records[key]['bd_id'] = row.bd_id

    return records


def get_day_data(cursor, records, register_date_str, login_date_str, day):
    sql = """SELECT COUNT(DISTINCT cdd_user_login_log.user_id) AS data, platform, channel, cdd_proxy_info.id AS proxy_id, cdd_bd_info.id 
                    AS bd_id
             FROM cdd_user_login_log
             JOIN cdd_user ON cdd_user_login_log.user_id = cdd_user.id
             JOIN cdd_channel_info ON cdd_user.channel = cdd_channel_info.id
             JOIN cdd_proxy_info ON cdd_channel_info.proxy_id = cdd_proxy_info.id
             JOIN cdd_bd_info ON cdd_proxy_info.bd_id = cdd_bd_info.id
             WHERE login_time::DATE = '{login_date}' 
                   AND cdd_user.id IN (SELECT id FROM cdd_user WHERE reg_time::DATE = '{register_date}')
             GROUP BY cdd_user.platform, cdd_user.channel, cdd_proxy_info.id, cdd_bd_info.id;
    """.format(login_date=login_date_str, register_date=register_date_str)
    cursor.execute(sql)
    rows = namedtuplefetchall(cursor)

    for row in rows:
        key = (row.platform, row.channel)
        if key not in records:
            _default = copy.deepcopy(default_data)
            records.setdefault(key, _default)
        records[key][day] = row.data

    return records


def generate_user_data(records, date_str):
    # 生成渠道数据
    for key, record in records.items():
        try:
            obj = UserDataDay.objects.get(platform=key[0], channel_id=key[1],
                                          report_date=datetime.strptime(date_str, '%Y-%m-%d'))
            obj.proxy_id = record['proxy_id']
            obj.bd_id = record['bd_id']
            obj.cps_data = record['cps_data']
            obj.cpa_data = record['cpa_data']
            obj.day1 = record['day1']
            obj.day3 = record['day3']
            obj.day7 = record['day7']
            obj.day15 = record['day15']
            obj.day30 = record['day30']
            obj.day60 = record['day60']
            obj.day90 = record['day90']
            obj.save()
        except UserDataDay.DoesNotExist:
            UserDataDay.objects.create(platform=key[0], channel_id=key[1], proxy_id=record['proxy_id'],
                                       bd_id=record['bd_id'], cps_data=record['cps_data'], cpa_data=record['cpa_data'],
                                       day1=record['day1'], day3=record['day3'], day7=record['day7'],
                                       day15=record['day15'], day30=record['day30'], day60=record['day60'],
                                       day90=record['day90'], report_date=datetime.strptime(date_str, '%Y-%m-%d'))

    return