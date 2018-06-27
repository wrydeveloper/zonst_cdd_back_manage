from django.db import models


class Admin(models.Model):
    """
    # 管理员表
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='', unique=True)
    role_id = models.IntegerField(default=0)
    status = models.IntegerField(default=1)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cdd_admin'
        ordering = ['-add_time']


class Role(models.Model):
    """
    # 角色表
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=100, default='')
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cdd_role'
        ordering = ['-add_time']


class Permission(models.Model):
    """
    # 权限表
    """

    id = models.AutoField(primary_key=True)
    parent_id = models.IntegerField(default=0)
    key = models.CharField(max_length=100, default='-')
    level = models.IntegerField(default=1)
    name = models.CharField(max_length=100, default='')
    url = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=100, default='')
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cdd_permission'
        ordering = ['id']


class RolePermission(models.Model):
    """
    # 角色权限对照表
    """

    id = models.AutoField(primary_key=True)
    role_id = models.IntegerField(default=0)
    permissions = models.CharField(max_length=500, default='')

    class Meta:
        db_table = 'cdd_role_permission'
