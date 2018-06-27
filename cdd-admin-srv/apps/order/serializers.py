from rest_framework import serializers

from . import models
from apps.lottery.models import NumberPeriodThirdparty
from utils.dict import play_type


class OrderNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderNumber
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(OrderNumberSerializer, self).to_representation(instance)

        try:
            period = NumberPeriodThirdparty.objects.get(lottery_alias=instance.lottery_alias,
                                                  lottery_period=instance.lottery_period)
        except NumberPeriodThirdparty.DoesNotExist:
            period = None

        tickets = []
        ticket_list = models.OrderNumberTicket.objects.filter(parent_order_id=instance.order_id).all()
        for ticket in ticket_list:
            d = {
                'play_type': play_type[instance.lottery_alias][ticket.play_type],
                'ante_code': ticket.ante_code,
                'amount': ticket.amount,
                'bonus_money': ticket.bonus_money,
                'total_money': ticket.total_money
            }
            tickets.append(d)

        ret.update({
            'bonus_code': period.bonus_code if period else '',
            'tickets': tickets,
            'order_time': instance.order_time.strftime('%Y-%m-%d %H:%M:%S')
        })

        return ret


class OrderNumberFollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderNumberFollow
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(OrderNumberFollowSerializer, self).to_representation(instance)

        ret.update({
            'order_time': instance.order_time.strftime('%Y-%m-%d %H:%M:%S')
        })

        return ret


class OrderNumberTicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderNumberTicket
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(OrderNumberTicketSerializer, self).to_representation(instance)

        ret.update({
            'order_time': instance.order_time.strftime('%Y-%m-%d %H:%M:%S')
        })

        return ret


class OrderSportsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderSports
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(OrderSportsSerializer, self).to_representation(instance)

        tickets = []
        ticket_list = models.OrderSportsDetail.objects.filter(order_id=instance.order_id)
        for ticket in ticket_list:
            d = {
                'match_number': ticket.match_number,
                'lottery_id': ticket.lottery_id,
                'play_type': play_type[instance.game][ticket.lottery_id],
                'league': ticket.league,
                'home_team': ticket.home_team,
                'away_team': ticket.away_team,
                'ft01_result': ticket.ft01_result,
                'ft02_result': ticket.ft02_result,
                'ft03_result': ticket.ft03_result,
                'ft04_result': ticket.ft04_result,
                'ft05_result': ticket.ft05_result,
                'bt01_result': ticket.bt01_result,
                'bt02_result': ticket.bt02_result,
                'bt03_result': ticket.bt03_result,
                'bt04_result': ticket.bt04_result
            }
            tickets.append(d)

        ret.update({
            'tickets': tickets,
            'order_time': instance.order_time.strftime('%Y-%m-%d %H:%M:%S')
        })

        return ret
