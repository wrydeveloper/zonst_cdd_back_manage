import os
import requests
from datetime import datetime

from django.conf import settings
from django.db.models import Sum

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.permissions import AdminPermission
from utils.md5 import encrypt

from . import models
from apps.user.models import User
from apps.config.models import Service
from . import serializers
from . import filters


class RechargeViewSet(viewsets.ModelViewSet):
    queryset = models.Recharge.objects.all()
    serializer_class = serializers.RechargeSerializer
    filter_class = filters.RechargeFilter
    permission_classes = (AdminPermission,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        total_money = queryset.aggregate(amount=Sum('charge_money')).get('amount')

        queryset = self.paginate_queryset(queryset)
        serializer = serializers.RechargeSerializer(queryset, many=True)

        data = {
            'statistic': {
                'total_money': total_money
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


class WithdrawViewSet(viewsets.ModelViewSet):
    queryset = models.Withdraw.objects.all()
    serializer_class = serializers.WithdrawSerializer
    filter_class = filters.WithdrawFilter
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super(WithdrawViewSet, self).get_queryset()

        if self.request.user.role == 'proxy':
            queryset = queryset.extra(
                tables=['cdd_user', 'cdd_channel_info'],
                where=[
                    'cdd_user.id = cdd_user_wallet_cash.user_id',
                    'cdd_channel_info.id = cdd_user.channel',
                    'cdd_channel_info.proxy_id = {proxy_id}'.format(proxy_id=self.request.user.id)
                ]
            )

        return queryset

    def list(self, request, *args, **kwargs):
        if self.request.user.role not in ('commerce', 'proxy'):
            return Response({'message': '您没有该权限！'}, status=status.HTTP_403_FORBIDDEN)

        queryset = self.filter_queryset(self.get_queryset())

        total_money = queryset.aggregate(amount=Sum('cash_money')).get('amount')

        queryset = self.paginate_queryset(queryset)
        serializer = serializers.WithdrawSerializer(queryset, many=True)

        data = {
            'statistic': {
                'total_money': total_money
            },
            'data': serializer.data
        }

        return self.get_paginated_response(data)

    @action(methods=('get',), detail=True, url_path='pass', permission_classes=(AdminPermission,))
    def handle_pass(self, request, **kwargs):
        if os.getenv('ENV') != 'pro':
            return Response({'message': '测试环境禁止提现！'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = models.Withdraw.objects.get(id=kwargs['pk'])
        except models.Withdraw.DoesNotExist:
            return Response({'message': '该记录不存在！'}, status=status.HTTP_400_BAD_REQUEST)

        if instance.status != 0:
            return Response({'message': '该提现已处理！'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=instance.user_id)
        except User.DoesNotExist:
            return Response({'message': '账户不存在！'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            service = Service.objects.get(id=1)
        except Service.DoesNotExist:
            return Response({'message': '服务不存在！'}, status=status.HTTP_400_BAD_REQUEST)

        url = settings.PAY_URL
        data = {
            'acc_type': '02',
            'payee_name': user.real_name,
            'payee_card_no': user.bank_card,
            'agent_pay_memo': '提现代付',
            'notify_url': settings.NOTIFY_URL,
            'order_number': instance.order_id,
            'order_amt': instance.cash_money,
            'bank_name': user.bank_name,
            'service_id': 1
        }

        sign = encrypt(data, service.secret_key)

        data.update({
            'sign': sign
        })

        try:
            r = requests.post(url, data=data)
        except requests.ConnectionError:
            return Response({'message': '请求代付接口网络错误！'}, status=status.HTTP_400_BAD_REQUEST)

        if r.status_code != 200:
            return Response({'message': '请求代付接口服务异常！'}, status=status.HTTP_400_BAD_REQUEST)

        code = r.json()['errno']
        if code != '0':
            return Response({'message': r.json()['errmsg']}, status=status.HTTP_400_BAD_REQUEST)

        instance.status = 3  # 已审核
        instance.save()

        return Response({'message': '操作成功！'})

    @action(methods=('get',), detail=True, url_path='reject', permission_classes=(AdminPermission,))
    def handle_reject(self, request, **kwargs):
        try:
            instance = models.Withdraw.objects.get(id=kwargs['pk'])
        except models.Withdraw.DoesNotExist:
            return Response({'message': '该记录不存在！'}, status=status.HTTP_400_BAD_REQUEST)

        if instance.status != 0:
            return Response({'message': '该提现已处理！'}, status=status.HTTP_400_BAD_REQUEST)

        instance.status = 2
        instance.status_message = '审核失败'
        instance.mark = '审核失败'
        instance.status_time = datetime.today()
        instance.save()

        return Response({'message': '操作成功！'})

    def create(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)


class BillViewSet(viewsets.ModelViewSet):
    queryset = models.Bill.objects.all()
    serializer_class = serializers.BillSerializer
    filter_class = filters.BillFilter
    permission_classes = (AdminPermission,)
