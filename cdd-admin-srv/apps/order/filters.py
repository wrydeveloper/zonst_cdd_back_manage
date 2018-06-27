from django.db.models import Q

import django_filters

from . import models


class OrderNumberFilter(django_filters.FilterSet):
    keyword = django_filters.CharFilter(method='filter_keyword')
    lottery_alias = django_filters.CharFilter(lookup_expr='iexact')
    order_status = django_filters.NumberFilter()
    is_followed_order = django_filters.NumberFilter()
    start_time = django_filters.DateTimeFilter(name='order_time', lookup_expr='gte')
    stop_time = django_filters.DateTimeFilter(name='order_time', lookup_expr='lte')

    class Meta:
        model = models.OrderNumber
        fields = ('followed_order_id', 'lottery_alias', 'order_status', 'is_followed_order', 'start_time', 'stop_time')

    def filter_keyword(self, queryset, name, value):
        if value:
            queryset = queryset.extra(
                tables=['cdd_user'],
                where=[
                    "cdd_user.id = cdd_lottery_order.user_id",
                    "(phone_number = '{value}'"
                    "OR cdd_user.id::TEXT = '{value}'"
                    "OR order_id = '{value}'"
                    "OR followed_order_id = '{value}')".format(value=value)
                ]
            )
        return queryset


class OrderNumberFollowFilter(django_filters.FilterSet):
    keyword = django_filters.CharFilter(method='filter_keyword')
    lottery_alias = django_filters.CharFilter(lookup_expr='iexact')
    follow_status = django_filters.NumberFilter()
    order_status = django_filters.NumberFilter()
    start_time = django_filters.DateTimeFilter(name='order_time', lookup_expr='gte')
    stop_time = django_filters.DateTimeFilter(name='order_time', lookup_expr='lte')

    class Meta:
        model = models.OrderNumberFollow
        fields = ('start_time', 'stop_time')

    def filter_keyword(self, queryset, name, value):
        if value:
            queryset = queryset.extra(
                tables=['cdd_user'],
                where=[
                    "cdd_user.id = cdd_lottery_order_follow.user_id",
                    "(phone_number = '{value}'"
                    "OR cdd_user.id::TEXT = '{value}'"
                    "OR order_id = '{value}')".format(value=value)
                ]
            )
        return queryset


class OrderSportsFilter(django_filters.FilterSet):
    keyword = django_filters.CharFilter(method='filter_keyword')
    game = django_filters.CharFilter(lookup_expr='iexact')
    order_status = django_filters.NumberFilter()
    start_time = django_filters.DateTimeFilter(name='order_time', lookup_expr='gte')
    stop_time = django_filters.DateTimeFilter(name='order_time', lookup_expr='lte')

    class Meta:
        model = models.OrderSports
        fields = ('game', 'order_status', 'start_time', 'stop_time')

    def filter_keyword(self, queryset, name, value):
        if value:
            queryset = queryset.extra(
                tables=['cdd_user'],
                where=[
                    "cdd_user.id = cdd_game_order.user_id",
                    "(phone_number = '{value}'"
                    "OR cdd_user.id::TEXT = '{value}'"
                    "OR order_id = '{value}')".format(value=value)
                ]
            )
        return queryset
