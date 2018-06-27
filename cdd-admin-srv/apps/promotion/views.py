from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.permissions import AdminPermission

from . import models
from . import serializers
from . import filters


class CommerceViewSet(viewsets.ModelViewSet):
    queryset = models.Commerce.objects.all()
    serializer_class = serializers.CommerceSerializer
    filter_class = filters.CommerceFilter
    permission_classes = (AdminPermission,)

    @action(methods=('get',), detail=False, url_path='options')
    def options(self, request, *args, **kwargs):
        serializer = serializers.CommerceOptionSerializer(self.get_queryset(), many=True)

        return Response(serializer.data)


class ProxyViewSet(viewsets.ModelViewSet):
    queryset = models.Proxy.objects.all()
    serializer_class = serializers.ProxySerializer
    filter_class = filters.ProxyFilter
    permission_classes = (AdminPermission,)

    @action(methods=('get',), detail=False, url_path='options')
    def options(self, request, *args, **kwargs):
        serializer = serializers.ProxyOptionSerializer(self.get_queryset(), many=True)

        return Response(serializer.data)


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = models.Channel.objects.all()
    serializer_class = serializers.ChannelSerializer
    filter_class = filters.ChannelFilter
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super(ChannelViewSet, self).get_queryset()

        if self.request.user.role == 'proxy':
            queryset = queryset.filter(proxy_id=self.request.user.id).all()

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = self.paginate_queryset(queryset)
        serializer = serializers.ChannelSerializer(queryset, many=True)

        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        context = {
            'user': request.user
        }
        serializer = serializers.ChannelSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': '添加成功！'})

    @action(methods=('get',), detail=False, url_path='options')
    def options(self, request, *args, **kwargs):
        serializer = serializers.ChannelOptionSerializer(self.get_queryset(), many=True)

        return Response(serializer.data)
