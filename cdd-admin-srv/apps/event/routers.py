from rest_framework_nested import routers

from . import views


router = routers.DefaultRouter()
router.register(r'points', views.PointViewSet, base_name='points')
