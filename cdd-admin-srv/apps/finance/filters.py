from django.db.models import Q

import django_filters

from . import models


class RechargeFilter(django_filters.FilterSet):
    keyword = django_filters.CharFilter(method='filter_keyword')
    pay_type = django_filters.NumberFilter()
    pay_status = django_filters.NumberFilter()
    start_time = django_filters.DateTimeFilter(name='order_time', lookup_expr='gte')
    stop_time = django_filters.DateTimeFilter(name='order_time', lookup_expr='lte')

    class Meta:
        model = models.Recharge
        fields = ('pay_type', 'pay_status', 'start_time', 'stop_time')

    def filter_keyword(self, queryset, name, value):
        if value:
            queryset = queryset.extra(
                tables=['cdd_user'],
                where=[
                    "cdd_wallet_recharge.user_id = cdd_user.id",
                    "(phone_number = '{value}'"
                    "OR order_id = '{value}'"
                    "OR cdd_user.id::TEXT = '{value}')".format(value=value)
                ]
            )
        return queryset


class WithdrawFilter(django_filters.FilterSet):
    keyword = django_filters.CharFilter(method='filter_keyword')
    status = django_filters.NumberFilter()
    start_time = django_filters.DateTimeFilter(name='req_time', lookup_expr='gte')
    stop_time = django_filters.DateTimeFilter(name='req_time', lookup_expr='lte')

    class Meta:
        model = models.Withdraw
        fields = ('status', 'start_time', 'stop_time')

    def filter_keyword(self, queryset, name, value):
        if value:
            queryset = queryset.extra(
                tables=['cdd_user'],
                where=[
                    "cdd_user_wallet_cash.user_id = cdd_user.id",
                    "(phone_number = '{value}'"
                    "OR order_id = '{value}'"
                    "OR cdd_user.id::TEXT = '{value}')".format(value=value)
                ]
            )
        return queryset


class BillFilter(django_filters.FilterSet):

    class Meta:
        model = models.Bill
        fields = ('user_id',)
