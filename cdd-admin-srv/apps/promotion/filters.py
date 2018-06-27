from django.db.models import Q

import django_filters

from . import models


class CommerceFilter(django_filters.FilterSet):
    keyword = django_filters.CharFilter(method='filter_keyword')
    start_time = django_filters.DateFilter(name='add_time', lookup_expr='gte')
    stop_time = django_filters.DateFilter(name='add_time', lookup_expr='lte')

    class Meta:
        model = models.Commerce
        fields = ('start_time', 'stop_time')

    def filter_keyword(self, queryset, name, value):
        if value:
            return queryset.filter(Q(bd_name__icontains=value) | Q(bd_id__icontains=value))
        return queryset


class ProxyFilter(django_filters.FilterSet):
    keyword = django_filters.CharFilter(method='filter_keyword')
    start_time = django_filters.DateTimeFilter(name='add_time', lookup_expr='gte')
    stop_time = django_filters.DateTimeFilter(name='add_time', lookup_expr='lte')

    class Meta:
        model = models.Proxy
        fields = ('bd_id', 'start_time', 'stop_time')

    def filter_keyword(self, queryset, name, value):
        if value:
            return queryset.filter(Q(proxy_name__icontains=value))
        return queryset


class ChannelFilter(django_filters.FilterSet):
    keyword = django_filters.CharFilter(method='filter_keyword')
    start_time = django_filters.DateFilter(name='add_time', lookup_expr='gte')
    stop_time = django_filters.DateFilter(name='add_time', lookup_expr='lte')

    class Meta:
        model = models.Channel
        fields = ('proxy_id', 'start_time', 'stop_time')

    def filter_keyword(self, queryset, name, value):
        if value:
            return queryset.filter(Q(id=value))
        return queryset
