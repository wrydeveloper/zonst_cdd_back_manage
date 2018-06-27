from rest_framework import serializers

from . import models


class RechargeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Recharge
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(RechargeSerializer, self).to_representation(instance)

        ret.update({
            'order_time': instance.order_time.strftime('%Y-%m-%d %H:%M:%S')
        })

        return ret


class WithdrawSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Withdraw
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(WithdrawSerializer, self).to_representation(instance)

        ret.update({
            'req_time': instance.req_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status_time': instance.status_time.strftime('%Y-%m-%d %H:%M:%S')
        })

        return ret


class BillSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Bill
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(BillSerializer, self).to_representation(instance)

        ret.update({
            'add_time': instance.add_time.strftime('%Y-%m-%d %H:%M:%S')
        })

        return ret
