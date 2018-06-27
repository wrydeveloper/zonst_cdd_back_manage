import django_filters

from . import models


class OrderFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(name='add_time', lookup_expr='gte')
    stop_time = django_filters.DateTimeFilter(name='add_time', lookup_expr='lte')

    class Meta:
        model = models.Order
        fields = ('start_time', 'stop_time')


class RefundFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(name='add_time', lookup_expr='gte')
    stop_time = django_filters.DateTimeFilter(name='add_time', lookup_expr='lte')

    class Meta:
        model = models.Refund
        fields = ('start_time', 'stop_time')
