from rest_framework_nested import routers

from . import views


router = routers.DefaultRouter()
router.register(r'menu', views.MenuViewSet, base_name='menu')
router.register(r'roles', views.RoleViewSet, base_name='roles')
router.register(r'permissions', views.PermissionViewSet, base_name='permissions')
router.register(r'admins', views.AdminViewSet, base_name='admins')
