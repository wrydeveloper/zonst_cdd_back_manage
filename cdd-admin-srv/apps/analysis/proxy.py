import copy
from datetime import datetime

from utils.sql import namedtuplefetchall

from .models import ProxyDataDay
from apps.promotion.models import Proxy

default_data = {
    'proxy_fee': 0,
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


def get_proxy_data(cursor, records, date_str):
    sql = """SELECT platform, proxy_id, SUM(cps_data) AS cps_data, SUM(cpa_data) AS cpa_data, SUM(cpd_data) AS cpd_data,
                    SUM(cpc_data) AS cpc_data, SUM(cpm_data) AS cpm_data, SUM(pay_user) AS pay_user,
                    SUM(order_count) AS order_count, SUM(coupon_fee) AS coupon_fee, SUM(charge_money) AS charge_money
             FROM cdd_channel_report_day
             JOIN cdd_channel_info ON cdd_channel_report_day.channel_id = cdd_channel_info.id
             WHERE report_date = '{date}'
             GROUP BY platform, proxy_id;""".format(date=date_str)
    cursor.execute(sql)
    rows = namedtuplefetchall(cursor)

    for row in rows:
        key = (row.platform, row.proxy_id)
        if key not in records:
            _default = copy.deepcopy(default_data)
            records.setdefault(key, _default)
        records[key]['cps_data'] = row.cps_data
        records[key]['cpa_data'] = row.cpa_data
        records[key]['cpd_data'] = row.cpd_data
        records[key]['cpc_data'] = row.cpc_data
        records[key]['cpm_data'] = row.cpm_data
        records[key]['pay_user'] = row.pay_user
        records[key]['order_count'] = row.order_count
        records[key]['coupon_fee'] = row.coupon_fee
        records[key]['charge_money'] = row.charge_money

    return records


def get_proxy_price(records):
    # 获取渠道价格
    for key, record in records.items():
        try:
            proxy = Proxy.objects.get(id=key[1])
        except Proxy.DoesNotExist:
            continue

        if proxy.proxy_type == 1:
            record['cps_rate'] = proxy.commission
        elif proxy.proxy_type == 2:
            record['cpa_price'] = proxy.commission
        elif proxy.proxy_type == 3:
            record['cpd_price'] = proxy.commission
        elif proxy.proxy_type == 4:
            record['cpc_price'] = proxy.commission
        elif proxy.proxy_type == 5:
            record['cpm_price'] = proxy.commission

        record['proxy_type'] = proxy.proxy_type

    return records


def compute_proxy_fee(records):
    # 计算代理成本
    for key, record in records.items():
        if record['proxy_type'] == 1:
            proxy_fee = record['cps_data'] * record['cps_rate'] // 100
        elif record['proxy_type'] == 2:
            proxy_fee = record['cpa_data'] * record['cpa_price']
        elif record['proxy_type'] == 3:
            proxy_fee = record['cpd_data'] * record['cpd_price']
        elif record['proxy_type'] == 4:
            proxy_fee = record['cpc_data'] * record['cpc_price']
        elif record['proxy_type'] == 5:
            proxy_fee = record['cpm_data'] * record['cpm_price']
        else:
            proxy_fee = 0

        record['proxy_fee'] = proxy_fee

    return records


def generate_proxy_data(records, date_str):
    # 生成代理数据
    for key, record in records.items():
        try:
            obj = ProxyDataDay.objects.get(proxy_id=key[1], platform=key[0],
                                           report_date=datetime.strptime(date_str, '%Y-%m-%d'))
            obj.proxy_fee = record['proxy_fee']
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
        except ProxyDataDay.DoesNotExist:
            ProxyDataDay.objects.create(proxy_id=key[1], platform=key[0], proxy_fee=record['proxy_fee'],
                                        coupon_fee=record['coupon_fee'], charge_money=record['charge_money'],
                                        cps_data=record['cps_data'], cpa_data=record['cpa_data'],
                                        cpd_data=record['cpd_data'], cpc_data=record['cpc_data'],
                                        cpm_data=record['cpm_data'], cps_rate=record['cps_rate'],
                                        cpa_price=record['cpa_price'], cpd_price=record['cpd_price'],
                                        cpc_price=record['cpc_price'], cpm_price=record['cpm_price'],
                                        pay_user=record['pay_user'], order_count=record['order_count'],
                                        report_date=datetime.strptime(date_str, '%Y-%m-%d'))

    return
