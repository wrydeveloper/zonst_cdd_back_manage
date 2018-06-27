import django_filters

from . import models

from django.db.models import Q


class NumberPeriodThirdpartyFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(lookup_expr='gte')
    stop_time = django_filters.DateTimeFilter(lookup_expr='lte')
    official_start_time = django_filters.DateTimeFilter(lookup_expr='gte')
    official_stop_time = django_filters.DateTimeFilter(lookup_expr='lte')
    lottery_alias = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = models.NumberPeriodThirdparty
        fields = ('start_time', 'stop_time', 'official_start_time', 'official_stop_time', 'lottery_alias')

class NumberPeriodLocalFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(lookup_expr='gte')
    stop_time = django_filters.DateTimeFilter(lookup_expr='lte')
    lottery_alias = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = models.NumberPeriodLocal
        fields = ('start_time', 'stop_time', 'lottery_alias')


class NumberLotteryBonusFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(name='add_time', lookup_expr='gte')
    stop_time = django_filters.DateTimeFilter(name='add_time', lookup_expr='lte')
    lottery_alias = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = models.NumberLotteryBonus
        fields = ('start_time', 'stop_time', 'lottery_alias')


class SportsLotteryMatchFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(name='add_time', lookup_expr='gte')
    stop_time = django_filters.DateTimeFilter(name='add_time', lookup_expr='lte')

    class Meta:
        model = models.SportsLotteryMatch
        fields = ('start_time' , 'stop_time')

class SportsLotteryBonusFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(name='bonus_date', lookup_expr='gte')
    stop_time = django_filters.DateTimeFilter(name='bonus_date', lookup_expr='lte')
    is_big_award = django_filters.NumberFilter(name='is_big_award')
    keyword = django_filters.CharFilter(method='filter_keyword')

    class Meta:
        model = models.SportsLotteryBonus
        fields = ('start_time', 'stop_time')

    def filter_keyword(self, queryset, name, value):
        if value:
            return queryset.filter(Q(scheme_id__icontains=value) | Q(match_number__icontains=value))
        return queryset
