import django_filters

from . import models


class ChannelDataDayFilter(django_filters.FilterSet):
    channel = django_filters.NumberFilter(name='channel_id')
    start_time = django_filters.DateFilter(name='report_date', lookup_expr='gte')
    stop_time = django_filters.DateFilter(name='report_date', lookup_expr='lte')

    class Meta:
        model = models.ChannelDataDay
        fields = ('channel', 'platform', 'start_time', 'stop_time')


class ProxyDataDayFilter(django_filters.FilterSet):
    proxy = django_filters.NumberFilter(name='proxy_id')
    start_time = django_filters.DateFilter(name='report_date', lookup_expr='gte')
    stop_time = django_filters.DateFilter(name='report_date', lookup_expr='lte')

    class Meta:
        model = models.ProxyDataDay
        fields = ('proxy', 'platform', 'start_time', 'stop_time')


class UserDataDayFilter(django_filters.FilterSet):
    bd = django_filters.NumberFilter(name='bd_id')
    channel = django_filters.NumberFilter(name='channel_id')
    proxy = django_filters.NumberFilter(name='proxy_id')
    start_time = django_filters.DateFilter(name='report_date', lookup_expr='gte')
    stop_time = django_filters.DateFilter(name='report_date', lookup_expr='lte')

    class Meta:
        model = models.UserDataDay
        fields = ('bd', 'channel', 'proxy', 'platform', 'start_time', 'stop_time')


class NumberBetDataDayFilter(django_filters.FilterSet):
    start_time = django_filters.DateFilter(name='report_date', lookup_expr='gte')
    stop_time = django_filters.DateFilter(name='report_date', lookup_expr='lte')

    class Meta:
        model = models.NumberBetDataDay
        fields = ('start_time', 'stop_time')


class SportsBetDataDayFilter(django_filters.FilterSet):
    start_time = django_filters.DateFilter(name='report_date', lookup_expr='gte')
    stop_time = django_filters.DateFilter(name='report_date', lookup_expr='lte')

    class Meta:
        model = models.SportsBetDataDay
        fields = ('start_time', 'stop_time')


class PayDataDayFilter(django_filters.FilterSet):
    start_time = django_filters.DateFilter(name='report_date', lookup_expr='gte')
    stop_time = django_filters.DateFilter(name='report_date', lookup_expr='lte')

    class Meta:
        model = models.PayDataDay
        fields = ('start_time', 'stop_time')
