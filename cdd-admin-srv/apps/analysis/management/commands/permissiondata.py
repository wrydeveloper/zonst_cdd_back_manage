from django.core.management.base import BaseCommand
from rest_framework.response import Response
from django.db import connection
from utils.sql import dictfetchall

class Command(BaseCommand):

    def handle(self, *args, **options):
        sql = '''
        insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 00:19:38.972543', '1', '0', '-', '', '首页', '/');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 00:58:41.233348', '1', '0', '-', '', '用户管理', '/user');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 00:59:17.231965', '1', '0', '-', '', '订单管理', '');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:05:41.345308', '2', '3', '3-', '', '数字彩订单', '/order/number');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:06:27.842742', '2', '3', '3-', '', '数字彩追号', '/order/number/follow');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:07:21.02273', '2', '3', '3-', '', '竞技彩订单', '/order/sports');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:08:07.650071', '1', '0', '-', '', '财务管理', '');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:08:24.465895', '2', '7', '7-', '', '充值列表', '/finance/recharge');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:12:22.552977', '2', '7', '7-', '', '提现列表', '/finance/withdraw');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:13:17.32342', '1', '0', '-', '', '数字彩管理', '');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:13:28.478538', '2', '10', '10-', '', '及众奖期', '/number/period/thirdparty');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:15:35.750593', '2', '10', '10-', '', '本地奖期', '/number/period/local');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:16:04.322697', '2', '10', '10-', '', '中奖信息', '/number/bonus');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:16:26.626022', '1', '0', '-', '', '竞技彩管理', '');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:17:46.911034', '2', '14', '14-', '', '竞彩赛事', '/sport/match');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:18:18.32919', '2', '14', '14-', '', '中奖信息', '/sport/bouns');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:20:24.606707', '1', '0', '-', '', '推广管理', '');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:21:01.772868', '2', '17', '17-', '', '商务', '/promotion/commerce');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:21:29.748602', '2', '17', '17-', '', '代理', '/promotion/proxy');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:22:20.587859', '2', '17', '17-', '', '渠道', '/promotion/channel');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:24:20.751128', '1', '0', '-', '', '数据分析', '');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:25:23.905916', '2', '21', '21-', '', '渠道分析', '/analysis/channel');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:25:42.900185', '2', '21', '21-', '', '用户分析', '/analysis/user');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:26:30.311584', '2', '21', '21-', '', '数字彩投注汇总', '/analysis/bet/number');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:26:55.169987', '2', '21', '21-', '', '竞技彩投注汇总', '/analysis/bet/sports');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:27:26.99453', '2', '21', '21-', '', '支付汇总', '/analysis/pay');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:41:08.082229', '1', '0', '-', '', '支付管理', '');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:41:51.946185', '2', '27', '27-', '', '订单列表', '/pay/order');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 01:42:31.885852', '2', '27', '27-', '', '退款列表', '/pay/refund');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 02:02:07.374519', '1', '0', '-', '', '配置管理', '');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 02:02:45.840617', '2', '30', '30-', '', '彩票列表', '/config/lottery');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 02:03:28.16072', '2', '30', '30-', '', '支付商渠道', '/config/pay/merchant');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 02:04:10.626654', '2', '30', '30-', '', '支付渠道列表', '/config/pay/channel');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 02:04:47.904556', '2', '30', '30-', '', '埋点设置', '/config/point');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 02:04:57.219542', '2', '30', '30-', '', 'Banner设置', '/config/banner');
insert into "public"."cdd_admin_permission" ( "add_time", "level", "parent_id", "key", "description", "name", "url") values ( '2018-06-12 09:23:29.517271', '2', '30', '30-', '', 'Apk上传', '/config/apk');
        '''
        cursor = connection.cursor()
        cursor.execute(sql)

        return