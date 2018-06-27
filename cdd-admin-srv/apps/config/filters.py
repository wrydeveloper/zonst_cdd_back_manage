import django_filters

from . import models


class LotteryFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(name='add_time', lookup_expr='gte')
    stop_time = django_filters.DateTimeFilter(name='add_time', lookup_expr='lte')

    class Meta:
        model = models.Lottery
        fields = ('start_time', 'stop_time')


class PayMerchantFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(name='add_time', lookup_expr='gte')
    stop_time = django_filters.DateTimeFilter(name='add_time', lookup_expr='lte')

    class Meta:
        model = models.PayMerchant
        fields = ('start_time', 'stop_time')


class PayChannelFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(name='add_time', lookup_expr='gte')
    stop_time = django_filters.DateTimeFilter(name='add_time', lookup_expr='lte')

    class Meta:
        model = models.PayChannel
        fields = ('start_time', 'stop_time')


class BannerFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(name='add_time', lookup_expr='gte')
    stop_time = django_filters.DateTimeFilter(name='add_time', lookup_expr='lte')

    class Meta:
        model = models.Banner
        fields = ('start_time', 'stop_time')


class BootPageFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(name='add_time', lookup_expr='gte')
    stop_time = django_filters.DateTimeFilter(name='add_time', lookup_expr='lte')

    class Meta:
        model = models.BootPage
        fields = ('start_time', 'stop_time')
