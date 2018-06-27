from django.db.models import Sum

from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.permissions import AdminPermission

from . import models
from . import serializers
from . import filters


class NumberPeriodThirdpartyViewSet(viewsets.ModelViewSet):
    queryset = models.NumberPeriodThirdparty.objects.all()
    serializer_class = serializers.NumberPeriodThirdpartySerializer
    filter_class = filters.NumberPeriodThirdpartyFilter
    permission_classes = (AdminPermission,)

    def create(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)


class NumberPeriodLocalViewSet(viewsets.ModelViewSet):
    queryset = models.NumberPeriodLocal.objects.all()
    serializer_class = serializers.NumberPeriodLocalSerializer
    filter_class = filters.NumberPeriodLocalFilter
    permission_classes = (AdminPermission,)

    def create(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)


class NumberLotteryBonusViewSet(viewsets.ModelViewSet):
    queryset = models.NumberLotteryBonus.objects.all()
    serializer_class = serializers.NumberLotteryBonusSerializer
    filter_class = filters.NumberLotteryBonusFilter
    permission_classes = (AdminPermission,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        bonus_money = queryset.aggregate(amount=Sum('bonus_money')).get('amount')

        queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)

        data = {
            'statistic': {
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


class SportsLotteryMatchViewSet(viewsets.ModelViewSet):
    queryset = models.SportsLotteryMatch.objects.all()
    serializer_class = serializers.SportsLotteryMatchSerilizer
    filter_class = filters.SportsLotteryMatchFilter
    permission_classes = (AdminPermission,)

    def create(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)


class SportsLotteryBonusViewSet(viewsets.ModelViewSet):
    queryset = models.SportsLotteryBonus.objects.all()
    serializer_class = serializers.SportsLotteryBonusSerilizer
    filter_class = filters.SportsLotteryBonusFilter
    permission_classes = (AdminPermission,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        bonus_money = queryset.aggregate(amount=Sum('bonus_money')).get('amount')
        win_money = queryset.aggregate(amount=Sum('win_money')).get('amount')

        queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)

        data = {
            'statistic': {
                'bonus_money': bonus_money,
                'win_money': win_money
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
