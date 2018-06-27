from rest_framework import serializers

from utils.dict import play_type

from . import models


class NumberPeriodThirdpartySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.NumberPeriodThirdparty
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(NumberPeriodThirdpartySerializer, self).to_representation(instance)

        ret.update({
            'add_time': instance.add_time.strftime('%Y-%m-%d %H:%M:%S'),
            'start_time': instance.start_time.strftime('%Y-%m-%d %H:%M'),
            'stop_time': instance.stop_time.strftime('%Y-%m-%d %H:%M'),
            'official_start_time': instance.official_start_time.strftime('%Y-%m-%d %H:%M'),
            'official_stop_time': instance.official_stop_time.strftime('%Y-%m-%d %H:%M')
        })

        return ret


class NumberPeriodLocalSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.NumberPeriodLocal
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(NumberPeriodLocalSerializer, self).to_representation(instance)

        ret.update({
            'add_time': instance.add_time.strftime('%Y-%m-%d %H:%M:%S'),
            'start_time': instance.start_time.strftime('%Y-%m-%d %H:%M'),
            'stop_time': instance.stop_time.strftime('%Y-%m-%d %H:%M')
        })

        return ret


class NumberLotteryBonusSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.NumberLotteryBonus
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(NumberLotteryBonusSerializer, self).to_representation(instance)

        ret.update({
            'play_type': play_type[instance.lottery_alias][instance.play_type],
            'add_time': instance.add_time.strftime('%Y-%m-%d %H:%M:%S')
        })

        return ret


class SportsLotteryMatchSerilizer(serializers.ModelSerializer):

    class Meta:
        model = models.SportsLotteryMatch
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(SportsLotteryMatchSerilizer,self).to_representation(instance)

        ret.update({
            'match_time':instance.match_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time':instance.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'add_time':instance.add_time.strftime('%Y-%m-%d %H:%M:%S'),
        })

        return ret


class SportsLotteryBonusSerilizer(serializers.ModelSerializer):

    class Meta:
        model = models.SportsLotteryBonus
        fields = '__all__'
