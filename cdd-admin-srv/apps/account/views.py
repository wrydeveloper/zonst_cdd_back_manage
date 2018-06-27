from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from . import serializers


class AccountViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    @action(methods=('post',), detail=False, url_path='token')
    def get_token(self, request):
        serializer = serializers.TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return Response(data)

    @action(methods=('get',), detail=False, permission_classes=(IsAuthenticated,), url_path='information')
    def get_information(self, request):
        serializer = serializers.ChannelInformationSerializer(request.user)

        return Response(serializer.data)

    @action(methods=('patch',), detail=False, permission_classes=(IsAuthenticated,), url_path='password')
    def change_password(self, request):
        """
        # 修改密码
        """
        serializer = serializers.ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request.user)

        return Response({'message': '修改成功!'})
