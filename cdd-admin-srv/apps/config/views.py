from rest_framework import viewsets, status

from apps.permissions import AdminPermission
from rest_framework.response import Response

from . import models
from . import serializers
from . import filters


class LotteryViewSet(viewsets.ModelViewSet):
    queryset = models.Lottery.objects.all()
    serializer_class = serializers.LotterySerializer
    filter_class = filters.LotteryFilter
    permission_classes = (AdminPermission,)


class PayMerchantViewSet(viewsets.ModelViewSet):
    queryset = models.PayMerchant.objects.all()
    serializer_class = serializers.PayMerchantSerializer
    filter_class = filters.PayMerchantFilter
    permission_classes = (AdminPermission,)


class PayChannelViewSet(viewsets.ModelViewSet):
    queryset = models.PayChannel.objects.all()
    serializer_class = serializers.PayChannelSerializer
    filter_class = filters.PayChannelFilter
    permission_classes = (AdminPermission,)


class BannerViewSet(viewsets.ModelViewSet):
    queryset = models.Banner.objects.all()
    serializer_class = serializers.BannerSerializer
    filter_class = filters.BannerFilter
    permission_classes = (AdminPermission,)


class BootPageViewSet(viewsets.ModelViewSet):
    queryset = models.BootPage.objects.all()
    serializer_class = serializers.BootPageSerializer
    filter_class = filters.BootPageFilter
    permission_classes = (AdminPermission,)

    def create(self, request, *args, **kwargs):
        serializer = serializers.BootPageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        try:
            bootpage = models.BootPage.objects.get(pk=kwargs['pk'])
        except models.BootPage.DoesNotExist:
            return Response({'message': '该记录不存在！'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.BootPageSerializer(bootpage, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)
