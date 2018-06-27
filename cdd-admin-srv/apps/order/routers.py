from rest_framework_nested import routers

from . import views


router = routers.DefaultRouter()
router.register(r'orders/number', views.OrderNumberViewSet, base_name='orders-number')
router.register(r'number/follows', views.OrderNumberFollowViewSet, base_name='number-follows')
router.register(r'orders/sports', views.OrderSportsViewSet, base_name='orders-sports')
