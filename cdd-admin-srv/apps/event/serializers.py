from rest_framework import serializers

from . import models


class PointSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Point
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(PointSerializer, self).to_representation(instance)

        ret.update({
            'created_at': instance.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

        return ret
