from rest_framework import viewsets

from apps.permissions import AdminPermission

from . import models
from . import serializers


class PointViewSet(viewsets.ModelViewSet):
    queryset = models.Point.objects.all()
    serializer_class = serializers.PointSerializer
    permission_classes = (AdminPermission,)

