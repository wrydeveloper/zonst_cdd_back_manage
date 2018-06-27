from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.permissions import AdminPermission
from utils.sql import namedtuplefetchall, dictfetchall
from django.db import connection
from . import models
from . import serializers


class MenuViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        if request.user.role == 'commerce':
            try:
                admin = models.Admin.objects.get(name=request.user.zonst_id)
            except models.Admin.DoesNotExist:
                return Response({'message': '该账户不存在！'}, status=status.HTTP_403_FORBIDDEN)
        else:
            try:
                admin = models.Admin.objects.get(name=request.user.id)
            except models.Admin.DoesNotExist:
                return Response({'message': '该账户不存在！'}, status=status.HTTP_403_FORBIDDEN)

        # 若角色id为0则代表具有所有的权限
        if admin.role_id == 0:
            queryset = models.Permission.objects.filter(parent_id=0).all()
            serializer = serializers.AllPermissionSerializer(queryset, many=True)
        else:
            try:
                role_permission = models.RolePermission.objects.get(role_id=admin.role_id)
            except models.RolePermission.DoesNotExist:
                return Response({'message': '该账户未分配权限！'}, status=status.HTTP_403_FORBIDDEN)

            permission_list = role_permission.permissions.split('|')

            level1_list = []
            queryset = models.Permission.objects.filter(id__in=permission_list)
            for obj in queryset:
                if obj.level == 1:
                    level1_list.append(obj.id)
                else:
                    level1_list.append(obj.parent_id)

            queryset = models.Permission.objects.filter(id__in=level1_list)
            serializer = serializers.PartialPermissionSerializer(queryset, many=True)
            level2 = models.Permission.objects.filter(id__in=permission_list).exclude(parent_id=0)
            for item in serializer.data:
                for obj in level2:
                    if obj.parent_id != item['id']:
                        continue
                    item['children'].append({
                        'id': obj.id,
                        'name': obj.name,
                        'url': obj.url
                    })

        return Response(serializer.data)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = serializers.RoleSerializer
    permission_classes = (AdminPermission,)


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = models.Permission.objects.all()
    serializer_class = serializers.AllPermissionSerializer
    permission_classes = (AdminPermission,)

    def list(self, request, *args, **kwargs):
        queryset = models.Permission.objects.filter(parent_id=0).all()
        serializer = serializers.AllPermissionSerializer(queryset, many=True)

        return Response(serializer.data)

class AdminViewSet(viewsets.ModelViewSet):
    queryset = models.Admin.objects.all()
    serializer_class = serializers.AdminRoleSerializer
    permission_classes = (AdminPermission,)





