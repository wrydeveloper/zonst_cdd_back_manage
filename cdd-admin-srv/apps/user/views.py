from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.permissions import AdminPermission

from .models import User
from .serializers import UserSerializer
from .filters import UserFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilter
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super(UserViewSet, self).get_queryset()

        if self.request.user.role == 'proxy':
            queryset = queryset.extra(
                tables=['cdd_channel_info'],
                where=[
                    'cdd_user.channel = cdd_channel_info.id',
                    'cdd_channel_info.proxy_id = {proxy_id}'.format(proxy_id=self.request.user.id)
                ]
            )
        elif self.request.user.role == 'channel':
            queryset = queryset.filter(channel=self.request.user.id).all()

        return queryset

    def list(self, request, *args, **kwargs):
        context = {
            'user': self.request.user
        }

        queryset = self.filter_queryset(self.get_queryset())

        total_count = queryset.count()
        h5_count = queryset.filter(platform=1).count()
        android_count = queryset.filter(platform=2).count()
        ios_count = queryset.filter(platform=3).count()

        queryset = self.paginate_queryset(queryset)
        serializer = UserSerializer(queryset, many=True, context=context)

        data = {
            'statistic': {
                'total_count': total_count,
                'h5_count': h5_count,
                'android_count': android_count,
                'ios_count': ios_count
            },
            'data': serializer.data
        }

        return self.get_paginated_response(data)

    def retrieve(self, request, *args, **kwargs):
        context = {
            'user': self.request.user
        }

        if self.request.user.role == 'channel':
            return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = self.get_queryset().get(id=kwargs['pk'])
        except User.DoesNotExist:
            return Response({'message': '该记录不存在！'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(instance, context=context)

        return Response(serializer.data)

    @action(methods=('patch',), detail=True, url_path='channel', permission_classes=(AdminPermission,))
    def change_channel(self, request, *args, **kwargs):
        try:
            instance = self.get_queryset().get(id=kwargs['pk'])
        except User.DoesNotExist:
            return Response({'message': '该记录不存在！'}, status=status.HTTP_400_BAD_REQUEST)

        instance.channel = request.data.get('channel', 100001)
        instance.bank_name = request.data.get('bank_name', instance.bank_name)
        instance.bank_card = request.data.get('bank_card', instance.bank_card)
        instance.bank_addr = request.data.get('bank_addr', instance.bank_addr)

        instance.save()

        return Response({'message': '操作成功！'})

    def create(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return Response({'message': '非法操作！'}, status=status.HTTP_400_BAD_REQUEST)
