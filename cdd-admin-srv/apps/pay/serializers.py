from rest_framework import serializers

from . import models


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(OrderSerializer, self).to_representation(instance)

        ret.update({
            'created_at': instance.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

        return ret


class RefundSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Refund
        fields = '__all__'
