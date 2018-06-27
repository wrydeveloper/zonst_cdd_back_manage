from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.permissions import AdminPermission

from . import models
from . import serializers
from . import filters


class OrderViewSet(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    filter_class = filters.OrderFilter
    permission_classes = (AdminPermission,)

    def create(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

class RefundViewSet(viewsets.ModelViewSet):
    queryset = models.Refund.objects.all()
    serializer_class = serializers.RefundSerializer
    filter_class = filters.RefundFilter
    permission_classes = (AdminPermission,)

    def create(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)
