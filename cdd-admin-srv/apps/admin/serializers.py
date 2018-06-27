from rest_framework import serializers

from . import models

from apps import errors


class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.ListField(write_only=True)

    class Meta:
        model = models.Role
        fields = '__all__'

    def create(self, validated_data):
        permissions = validated_data.pop('permissions', [])

        instance = super(RoleSerializer, self).create(validated_data)

        permissions = '|'.join([str(i) for i in permissions])
        models.RolePermission.objects.create(role_id=instance.id, permissions=permissions)

        return instance

    def update(self, instance, validated_data):
        permissions = validated_data.pop('permissions', [])

        try:
            role_permission = models.RolePermission.objects.get(role_id=instance.id)
        except models.RolePermission.DoesNotExist:
            raise errors.raise_server_error('非法数据！')

        role_permission.permissions = '|'.join([str(i) for i in permissions])
        role_permission.save()

        instance = super(RoleSerializer, self).update(instance, validated_data)

        return instance

    def to_representation(self, instance):
        ret = super(RoleSerializer, self).to_representation(instance)

        try:
            role_permission = models.RolePermission.objects.get(role_id=instance.id)
            permissions = role_permission.permissions.split('|') if role_permission.permissions else []
        except models.RolePermission.DoesNotExist:
            permissions = []

        ret.update({
            'add_time': instance.add_time.strftime('%Y-%m-%d %H:%M:%S'),
            'permissions': [int(i) for i in permissions] if permissions else []
        })

        return ret


class AllPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Permission
        fields = ('id', 'name', 'url')

    def to_representation(self, instance):
        ret = super(AllPermissionSerializer, self).to_representation(instance)

        children = models.Permission.objects.filter(parent_id=instance.id)
        serializer = AllPermissionSerializer(children, many=True)

        ret.update({
            'children': serializer.data
        })

        return ret


class PartialPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Permission
        fields = ('id', 'name', 'url')

    def to_representation(self, instance):
        ret = super(PartialPermissionSerializer, self).to_representation(instance)

        ret.update({
            'children': []
        })

        return ret

class AdminRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Admin
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(AdminRoleSerializer, self).to_representation(instance)

        if instance.role_id is 0:
            role_name = '未分配权限'
        else:
            role_name = models.Role.objects.get(id=instance.role_id).name

        ret.update({
            'add_time': instance.add_time.strftime('%Y-%m-%d %H:%M:%S'),
            'role_name': role_name
        })

        return ret