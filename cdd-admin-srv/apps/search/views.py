from django.db import connection
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response

from apps.permissions import AdminPermission

from utils.sql import namedtuplefetchall, dictfetchall


class SearchResultView(APIView):
    permission_classes = (AdminPermission,)

    def get(self, request):
        try:
            lottery = request.GET['lottery']
            keyword = request.GET['keyword']
        except Exception as e:
            return Response({'message': '参数不完整！'})

        page = int(request.GET.get('page', 1))
        page_size = settings.REST_FRAMEWORK['PAGE_SIZE']

        offset = (page - 1) * page_size

        cursor = connection.cursor()

        if lottery == 'number':
            data_sql = """SELECT user_id, cdd_lottery_order.id AS order_pk, order_id, lottery_alias, amount, total_money, bonus_money, order_status, order_time
                          FROM cdd_lottery_order
                          JOIN cdd_user ON cdd_lottery_order.user_id = cdd_user.id
                          WHERE CAST(cdd_user.id AS TEXT) LIKE '{keyword}' OR cdd_user.nick_name ~ '{keyword}' OR 
                                cdd_user.id_card ~ '{keyword}' OR cdd_user.bank_card ~ '{keyword}' OR 
                                order_id ~ '{keyword}' OR lottery_period ~ '{keyword}'
                          LIMIT {page_size} OFFSET {offset}""".format(keyword=keyword, page_size=page_size, offset=offset)
            count_sql = """SELECT COUNT(1) AS count
                           FROM cdd_lottery_order
                           JOIN cdd_user ON cdd_lottery_order.user_id = cdd_user.id
                           WHERE CAST(cdd_user.id AS TEXT) LIKE '{keyword}' OR cdd_user.nick_name ~ '{keyword}' OR 
                                 cdd_user.id_card ~ '{keyword}' OR cdd_user.bank_card ~ '{keyword}' OR 
                                 order_id ~ '{keyword}' OR lottery_period ~ '{keyword}'""".format(keyword=keyword)
        else:
            data_sql = """SELECT user_id, cdd_game_order.id AS order_pk, order_id, game, bet_multi, bet_type, bet_money, bonus_money, order_status, order_time
                          FROM cdd_game_order
                          JOIN cdd_user ON cdd_game_order.user_id = cdd_user.id
                          WHERE CAST(cdd_user.id AS TEXT) LIKE '{keyword}' OR cdd_user.nick_name ~ '{keyword}' OR 
                                cdd_user.id_card ~ '{keyword}' OR cdd_user.bank_card ~ '{keyword}' OR 
                                order_id ~ '{keyword}'
                          LIMIT {page_size} OFFSET {offset}""".format(keyword=keyword, page_size=page_size, offset=offset)
            count_sql = """SELECT COUNT(1) AS count
                           FROM cdd_game_order
                           JOIN cdd_user ON cdd_game_order.user_id = cdd_user.id
                           WHERE CAST(cdd_user.id AS TEXT) LIKE '{keyword}' OR cdd_user.nick_name ~ '{keyword}' OR 
                                 cdd_user.id_card ~ '{keyword}' OR cdd_user.bank_card ~ '{keyword}' OR 
                                 order_id ~ '{keyword}'""".format(keyword=keyword)


        cursor.execute(data_sql)
        data_rows = dictfetchall(cursor)
        for row in data_rows:
            row['order_time'] = row['order_time'].strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute(count_sql)
        count_rows = namedtuplefetchall(cursor)
        count = count_rows[0].count

        data = {
            'count': count,
            'data': data_rows
        }

        return Response(data)
