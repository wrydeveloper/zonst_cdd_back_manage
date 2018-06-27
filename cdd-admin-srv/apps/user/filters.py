from django.db.models import Q

import django_filters

from .models import User


class UserFilter(django_filters.FilterSet):
    keyword = django_filters.CharFilter(method='filter_keyword')
    channel = django_filters.CharFilter()
    platform = django_filters.NumberFilter()
    start_time = django_filters.DateTimeFilter(name='reg_time', lookup_expr='gte')
    stop_time = django_filters.DateTimeFilter(name='reg_time', lookup_expr='lte')

    class Meta:
        model = User
        fields = ('platform', 'channel', 'start_time', 'stop_time', 'inviter_id')

    def filter_keyword(self, queryset, name, value):
        if value:
            return queryset.filter(Q(phone_number__icontains=value) | Q(real_name__icontains=value) |
                                   Q(nick_name__icontains=value) | Q(bank_card__icontains=value) |
                                   Q(id__icontains=value))
        return queryset
