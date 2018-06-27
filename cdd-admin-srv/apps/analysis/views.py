from datetime import datetime, timedelta

from django.db import connection
from django.db.models import Sum

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.permissions import AdminPermission
from utils.sql import namedtuplefetchall, dictfetchall

from . import models
from . import serializers
from . import filters


class ChannelDataDayViewSet(viewsets.ModelViewSet):
    queryset = models.ChannelDataDay.objects.all()
    serializer_class = serializers.ChannelDataDaySerializer
    filter_class = filters.ChannelDataDayFilter
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super(ChannelDataDayViewSet, self).get_queryset()

        if self.request.user.role == 'proxy':
            queryset = queryset.extra(
                tables=['cdd_channel_info'],
                where=[
                    'cdd_channel_report_day.channel_id = cdd_channel_info.id',
                    'cdd_channel_info.proxy_id = {proxy_id}'.format(proxy_id=self.request.user.id)
                ]
            )
        elif self.request.user.role == 'channel':
            queryset = queryset.filter(channel_id=self.request.user.id).all()

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        statistic = queryset.aggregate(cps_data=Sum('cps_data'), channel_fee=Sum('channel_fee'),
                                       coupon_fee=Sum('coupon_fee'), charge_money=Sum('charge_money'))

        queryset = self.paginate_queryset(queryset)
        serializer = serializers.ChannelDataDaySerializer(queryset, many=True)

        data = {
            'statistic': {
                'cps_data': statistic.get('cps_data'),
                'channel_fee': statistic.get('channel_fee'),
                'coupon_fee': statistic.get('coupon_fee'),
                'charge_money': statistic.get('charge_money')
            },
            'data': serializer.data
        }

        return self.get_paginated_response(data)

    def create(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)


class ProxyDataDayViewSet(viewsets.ModelViewSet):
    queryset = models.ProxyDataDay.objects.all()
    serializer_class = serializers.ProxyDataDaySerializer
    filter_class = filters.ProxyDataDayFilter
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super(ProxyDataDayViewSet, self).get_queryset()

        if self.request.user.role == 'proxy':
            queryset = queryset.filter(proxy_id=self.request.user.id)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        statistic = queryset.aggregate(cps_data=Sum('cps_data'), proxy_fee=Sum('proxy_fee'),
                                       coupon_fee=Sum('coupon_fee'), charge_money=Sum('charge_money'))

        queryset = self.paginate_queryset(queryset)
        serializer = serializers.ProxyDataDaySerializer(queryset, many=True)

        data = {
            'statistic': {
                'cps_data': statistic.get('cps_data'),
                'proxy_fee': statistic.get('proxy_fee'),
                'coupon_fee': statistic.get('coupon_fee'),
                'charge_money': statistic.get('charge_money')
            },
            'data': serializer.data
        }

        return self.get_paginated_response(data)

    def create(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)


class UserDataDayViewSet(viewsets.ModelViewSet):
    queryset = models.UserDataDay.objects.all()
    serializer_class = serializers.UserDataDaySerializer
    filter_class = filters.UserDataDayFilter
    permission_classes = (AdminPermission,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        statistic = queryset.aggregate(cps_data=Sum('cps_data'))

        queryset = self.paginate_queryset(queryset)
        serializer = serializers.UserDataDaySerializer(queryset, many=True)

        data = {
            'statistic': {
                'cps_data': statistic.get('cps_data')
            },
            'data': serializer.data
        }

        return self.get_paginated_response(data)

    def create(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)


class NumberBetDataDayViewSet(viewsets.ModelViewSet):
    queryset = models.NumberBetDataDay.objects.all()
    serializer_class = serializers.NumberBetDataDaySerializer
    filter_class = filters.NumberBetDataDayFilter
    permission_classes = (AdminPermission,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        statistic = queryset.aggregate(total_money=Sum('total_money'))

        queryset = self.paginate_queryset(queryset)
        serializer = serializers.NumberBetDataDaySerializer(queryset, many=True)

        data = {
            'statistic': {
                'total_money': statistic.get('total_money')
            },
            'data': serializer.data
        }

        return self.get_paginated_response(data)

    def create(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)


class SportsBetDataDayViewSet(viewsets.ModelViewSet):
    queryset = models.SportsBetDataDay.objects.all()
    serializer_class = serializers.SportsBetDataDaySerializer
    filter_class = filters.SportsBetDataDayFilter
    permission_classes = (AdminPermission,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        statistic = queryset.aggregate(total_money=Sum('total_money'))

        queryset = self.paginate_queryset(queryset)
        serializer = serializers.SportsBetDataDaySerializer(queryset, many=True)

        data = {
            'statistic': {
                'total_money': statistic.get('total_money')
            },
            'data': serializer.data
        }

        return self.get_paginated_response(data)

    def create(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)


class PayDataDayViewSet(viewsets.ModelViewSet):
    queryset = models.PayDataDay.objects.all()
    serializer_class = serializers.PayDataDaySerializer
    filter_class = filters.PayDataDayFilter
    permission_classes = (AdminPermission,)

    def create(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)


class ChartUserView(APIView):
    permission_classes = (AdminPermission,)

    def get(self, request):
        cursor = connection.cursor()

        date_str = datetime.today().strftime('%Y-%m-%d')
        register_date_str = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

        platform_dict = {
            1: 0,
            2: 0,
            3: 0
        }

        sql = """SELECT COUNT(1) AS count, platform
                 FROM cdd_user
                 WHERE reg_time::DATE = '{date}'
                 GROUP BY platform;""".format(date=date_str)
        cursor.execute(sql)
        rows = namedtuplefetchall(cursor)
        total_count = 0
        for row in rows:
            total_count += row.count
            platform_dict[row.platform] = row.count

        sql = """SELECT COUNT(DISTINCT user_id) AS login_count
                 FROM cdd_user_login_log
                 WHERE login_time::DATE = '{login_date}' 
                 AND user_id IN (SELECT id FROM cdd_user WHERE reg_time::DATE = '{register_date}');
        """.format(login_date=date_str, register_date=register_date_str)
        cursor.execute(sql)
        login_count = namedtuplefetchall(cursor)[0].login_count

        data = {
            'h5_count': platform_dict[1],
            'android_count': platform_dict[2],
            'ios_count': platform_dict[3],
            'total_count': total_count,
            'rate': round(login_count / total_count * 100, 2) if total_count else 0
        }
        
        return Response(data)


class ChartNumberView(APIView):
    permission_classes = (AdminPermission,)

    def get(self, request):
        cursor = connection.cursor()

        date_str = datetime.today().strftime('%Y-%m-%d')

        platform_dict = {
            1: 0,
            2: 0,
            3: 0
        }

        # 统计订单金额
        sql = """SELECT SUM(total_money) AS money, cdd_user.platform
                 FROM cdd_lottery_order_ticket
                 JOIN cdd_user ON cdd_lottery_order_ticket.user_id = cdd_user.id
                 WHERE order_date = '{date}' AND cdd_lottery_order_ticket.ticket_status = '0000'
                 GROUP BY cdd_user.platform;""".format(date=date_str)
        cursor.execute(sql)
        rows = namedtuplefetchall(cursor)
        total_money = 0
        for row in rows:
            total_money += row.money
            platform_dict[row.platform] = row.money

        # 统计下单人次
        sql = """SELECT COUNT(DISTINCT cdd_lottery_order_ticket.user_id) AS user_count
                 FROM cdd_lottery_order_ticket
                 JOIN cdd_user ON cdd_lottery_order_ticket.user_id = cdd_user.id
                 WHERE cdd_lottery_order_ticket.order_date = '{date}';""".format(date=date_str)
        cursor.execute(sql)
        user_count = namedtuplefetchall(cursor)[0].user_count

        # 统计订单数
        sql = """SELECT COUNT(1) AS order_count
                 FROM cdd_lottery_order_ticket
                 WHERE order_date = '{date}';""".format(date=date_str)
        cursor.execute(sql)
        order_count = namedtuplefetchall(cursor)[0].order_count

        # 统计柱状图
        date_dict = {}
        for i in range(1, 31):
            key = (datetime.today() - timedelta(days=i)).strftime('%Y-%m-%d')
            date_dict[key] = 0

        start_date = (datetime.today() - timedelta(days=31)).strftime('%Y-%m-%d')
        end_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        sql = """SELECT SUM(total_money) / 100 AS money, CAST(report_date AS TEXT) AS date_str
                 FROM cdd_number_bet_report_day
                 WHERE report_date >= '{start_date}' AND report_date <= '{end_date}'
                 GROUP BY report_date;""".format(start_date=start_date, end_date=end_date)
        cursor.execute(sql)
        rows = namedtuplefetchall(cursor)
        for row in rows:
            date_dict[row.date_str] = row.money

        chart_data = []
        for key, value in date_dict.items():
            d = {
                'date': key,
                'money': value
            }
            chart_data.append(d)

        data = {
            'total_money': total_money,
            'h5_money': platform_dict[1],
            'android_money': platform_dict[2],
            'ios_money': platform_dict[3],
            'user_count': user_count,
            'order_count': order_count,
            'chart_data': chart_data
        }

        return Response(data)


class ChartSportsView(APIView):
    permission_classes = (AdminPermission,)

    def get(self, request):
        cursor = connection.cursor()

        date_str = datetime.today().strftime('%Y-%m-%d')

        platform_dict = {
            1: 0,
            2: 0,
            3: 0
        }

        # 统计订单金额
        sql = """SELECT SUM(bet_money) AS money, cdd_user.platform 
                 FROM cdd_game_order
                 JOIN cdd_user ON cdd_game_order.user_id = cdd_user.id
                 WHERE order_date = '{date}' AND order_status IN (2, 5, 6)
                 GROUP BY cdd_user.platform;""".format(date=date_str)
        cursor.execute(sql)
        rows = namedtuplefetchall(cursor)
        total_money = 0
        for row in rows:
            total_money += row.money
            platform_dict[row.platform] = row.money

        # 统计下单人次
        sql = """SELECT COUNT(DISTINCT cdd_game_order.user_id) AS user_count
                 FROM cdd_game_order
                 JOIN cdd_user ON cdd_game_order.user_id = cdd_user.id
                 WHERE cdd_game_order.order_date = '{date}';""".format(date=date_str)
        cursor.execute(sql)
        user_count = namedtuplefetchall(cursor)[0].user_count

        # 统计订单数
        sql = """SELECT COUNT(1) AS order_count
                 FROM cdd_game_order
                 WHERE order_date = '{date}';""".format(date=date_str)
        cursor.execute(sql)
        order_count = namedtuplefetchall(cursor)[0].order_count

        # 统计柱状图
        date_dict = {}
        for i in range(1, 31):
            key = (datetime.today() - timedelta(days=i)).strftime('%Y-%m-%d')
            date_dict[key] = 0

        start_date = (datetime.today() - timedelta(days=31)).strftime('%Y-%m-%d')
        end_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        sql = """SELECT SUM(total_money) / 100 AS money, CAST(report_date AS TEXT) AS date_str
                 FROM cdd_sports_bet_report_day
                 WHERE report_date >= '{start_date}' AND report_date <= '{end_date}'
                 GROUP BY report_date;""".format(start_date=start_date, end_date=end_date)
        cursor.execute(sql)
        rows = namedtuplefetchall(cursor)
        for row in rows:
            date_dict[row.date_str] = row.money

        chart_data = []
        for key, value in date_dict.items():
            d = {
                'date': key,
                'money': value
            }
            chart_data.append(d)

        data = {
            'total_money': total_money,
            'h5_money': platform_dict[1],
            'android_money': platform_dict[2],
            'ios_money': platform_dict[3],
            'user_count': user_count,
            'order_count': order_count,
            'chart_data': chart_data
        }

        return Response(data)


class ChartSalesTrendView(APIView):

    def get(self, requset):
        cursor = connection.cursor()

        month_dict = {}
        for i in range(12):
            key = '{i}月'.format(i=i)
            month_dict[key] = 0

        sql = """SELECT EXTRACT(MONTH from report_date) as month, SUM(cps_data) as cps
                 FROM cdd_channel_report_day
                 GROUP BY EXTRACT(MONTH from report_date);"""
        cursor.execute(sql)
        rows = namedtuplefetchall(cursor)
        for row in rows:
            key = ''.join([str(int(row.month)), '月'])
            month_dict[key] = row.cps

        chart_data = []
        for key, value in month_dict.items():
            d = {
                'month': key,
                'money': value / 100
            }
            chart_data.append(d)

        data = {
            'chart_data': chart_data
        }

        return Response(data)


class ChartSalesRankView(APIView):

    def get(self, request):
        sdate = request.GET.get('sdate', (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'))
        edate = request.GET.get('edate', (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'))

        sql = """SELECT SUM(cps_data) as cps, channel_id 
                 FROM cdd_channel_report_day 
                 WHERE report_date >= '{sdate}' AND report_date <= '{edate}'
                 GROUP BY channel_id 
                 ORDER BY SUM(cps_data) DESC LIMIT 10 OFFSET 0;""".format(sdate=sdate, edate=edate)

        cursor = connection.cursor()
        cursor.execute(sql)
        data = dictfetchall(cursor)

        return Response(data)


class ChartUserH5TransformView(APIView):

    def get(self, request):
        sdate = request.GET.get('sdate', (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'))
        edate = request.GET.get('edate', (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'))

        transform_dict = {
            'register': 0
        }

        sql = """SELECT SUM(cpa_data) AS register, report_date
                 FROM cdd_channel_report_day 
                 WHERE report_date >= '{sdate}' AND report_date <= '{edate}' AND platform = 1
                 GROUP BY report_date;""".format(sdate=sdate, edate=edate)

        cursor = connection.cursor()
        cursor.execute(sql)
        rows = namedtuplefetchall(cursor)
        if rows:
            transform_dict['register'] = rows[0].register

        chart_data = [
            {'action': '注册', 'value': transform_dict['register']}
        ]

        data = {
            'chart_data': chart_data
        }

        return Response(data)


class ChartUserMobileTransformView(APIView):

    def get(self, request):
        sdate = request.GET.get('sdate', (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'))
        edate = request.GET.get('edate', (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'))

        transform_dict = {
            'install': 0,
            'register': 0
        }

        sql = """SELECT SUM(cpd_data) AS install, SUM(cpa_data) AS register, report_date
                 FROM cdd_channel_report_day 
                 WHERE report_date >= '{sdate}' AND report_date <= '{edate}' AND platform <> 1
                 GROUP BY report_date;""".format(sdate=sdate, edate=edate)

        cursor = connection.cursor()
        cursor.execute(sql)
        rows = namedtuplefetchall(cursor)
        if rows:
            transform_dict['install'] = rows[0].install
            transform_dict['register'] = rows[0].register

        chart_data = [
            {'action': '安装', 'value': transform_dict['install']},
            {'action': '注册', 'value': transform_dict['register']}
        ]

        data = {
            'chart_data': chart_data
        }

        return Response(data)


class ChartSalesScaleView(APIView):

    def get(self, request):
        sdate = request.GET.get('sdate', (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'))
        edate = request.GET.get('edate', (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'))

        lottery_dict = {'FT': 0, 'BT': 0, 'dlc': 0, 'JXK3': 0, '3d': 0, 'dlt': 0, 'ssq': 0}

        # 统计数字彩
        sql = """SELECT SUM(total_money) AS money, lottery_alias
                 FROM cdd_lottery_order
                 WHERE order_date >= '{sdate}' AND order_date <= '{edate}'
                 GROUP BY lottery_alias;""".format(sdate=sdate, edate=edate)

        cursor = connection.cursor()
        cursor.execute(sql)
        rows = namedtuplefetchall(cursor)

        number_money = 0
        for row in rows:
            number_money += row.money
            lottery_dict[row.lottery_alias] = row.money

        # 统计竞技彩
        sql = """SELECT SUM(bet_money) AS money, game AS lottery_alias
                 FROM cdd_game_order 
                 WHERE order_date >= '{sdate}' AND order_date <= '{edate}'
                 GROUP BY game;""".format(sdate=sdate, edate=edate)

        cursor = connection.cursor()
        cursor.execute(sql)
        rows = namedtuplefetchall(cursor)

        sports_money = 0
        for row in rows:
            sports_money += row.money
            lottery_dict[row.lottery_alias] = row.money

        total_money = number_money + sports_money

        chart_data = [
            {'item': '竞彩足球', 'count': lottery_dict['FT']},
            {'item': '竞彩篮球', 'count': lottery_dict['BT']},
            {'item': '多乐彩', 'count': lottery_dict['dlc']},
            {'item': "新快3", 'count': lottery_dict['JXK3']},
            {'item': "福彩3D", 'count': lottery_dict['3d']},
            {'item': "大乐透", 'count': lottery_dict['dlt']},
            {'item': "双色球", 'count': lottery_dict['ssq']}
        ]

        data = {
            'chart_data': chart_data,
            'total_money': total_money / 100
        }

        return Response(data)
