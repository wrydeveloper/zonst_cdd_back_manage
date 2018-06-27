from rest_framework_nested import routers

from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, base_name='users')
