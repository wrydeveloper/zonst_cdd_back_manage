from django.db.models import Sum

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from . import models
from . import serializers
from . import filters


class OrderNumberViewSet(viewsets.ModelViewSet):
    queryset = models.OrderNumber.objects.all()
    serializer_class = serializers.OrderNumberSerializer
    filter_class = filters.OrderNumberFilter
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super(OrderNumberViewSet, self).get_queryset()

        if self.request.user.role == 'proxy':
            queryset = queryset.extra(
                tables=['cdd_user', 'cdd_channel_info'],
                where=[
                    'cdd_lottery_order.user_id = cdd_user.id',
                    'cdd_user.channel = cdd_channel_info.id',
                    'cdd_channel_info.proxy_id = {proxy_id}'.format(proxy_id=self.request.user.id)
                ]
            )
        elif self.request.user.role == 'channel':
            queryset = queryset.extra(
                tables=['cdd_user'],
                where=[
                    'cdd_lottery_order.user_id = cdd_user.id',
                    'cdd_user.channel = {channel_id}'.format(channel_id=self.request.user.id)
                ]
            )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        total_count = queryset.count()
        total_money = queryset.aggregate(amount=Sum('total_money')).get('amount')
        bonus_money = queryset.aggregate(amount=Sum('bonus_money')).get('amount')

        queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)

        data = {
            'statistic': {
                'total_count': total_count,
                'total_money': total_money,
                'bonus_money': bonus_money
            },
            'data': serializer.data
        }

        return self.get_paginated_response(data)

    @action(methods=('get',), detail=False, url_path='follows')
    def list_follow(self, request, **kwargs):
        queryset = models.OrderNumberFollow.objects.filter(order_id=kwargs['pk']).all()
        queryset = filters.OrderNumberFollowFilter(request.GET, queryset=queryset).qs
        queryset = self.paginate_queryset(queryset)
        serializer = serializers.OrderNumberFollowSerializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)


class OrderNumberFollowViewSet(viewsets.ModelViewSet):
    queryset = models.OrderNumberFollow.objects.all()
    serializer_class = serializers.OrderNumberFollowSerializer
    filter_class = filters.OrderNumberFollowFilter
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super(OrderNumberFollowViewSet, self).get_queryset()

        if self.request.user.role == 'proxy':
            queryset = queryset.extra(
                tables=['cdd_user', 'cdd_channel_info'],
                where=[
                    'cdd_lottery_order_follow.user_id = cdd_user.id',
                    'cdd_user.channel = cdd_channel_info.id',
                    'cdd_channel_info.proxy_id = {proxy_id}'.format(proxy_id=self.request.user.id)
                ]
            )
        elif self.request.user.role == 'channel':
            queryset = queryset.extra(
                tables=['cdd_user'],
                where=[
                    'cdd_lottery_order_follow.user_id = cdd_user.id',
                    'cdd_user.channel = {channel_id}'.format(channel_id=self.request.user.id)
                ]
            )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        total_money = queryset.aggregate(amount=Sum('total_money')).get('amount')

        queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)

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


class OrderSportsViewSet(viewsets.ModelViewSet):
    queryset = models.OrderSports.objects.all()
    serializer_class = serializers.OrderSportsSerializer
    filter_class = filters.OrderSportsFilter
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super(OrderSportsViewSet, self).get_queryset()

        if self.request.user.role == 'proxy':
            queryset = queryset.extra(
                tables=['cdd_user', 'cdd_channel_info'],
                where=[
                    'cdd_game_order.user_id = cdd_user.id',
                    'cdd_user.channel = cdd_channel_info.id',
                    'cdd_channel_info.proxy_id = {proxy_id}'.format(proxy_id=self.request.user.id)
                ]
            )
        elif self.request.user.role == 'channel':
            queryset = queryset.extra(
                tables=['cdd_user'],
                where=[
                    'cdd_game_order.user_id = cdd_user.id',
                    'cdd_user.channel = {channel_id}'.format(channel_id=self.request.user.id)
                ]
            )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        total_count = queryset.count()
        total_money = queryset.aggregate(amount=Sum('bet_money')).get('amount')
        bonus_money = queryset.aggregate(amount=Sum('bonus_money')).get('amount')

        queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)

        data = {
            'statistic': {
                'total_count': total_count,
                'total_money': total_money,
                'bonus_money': bonus_money
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
