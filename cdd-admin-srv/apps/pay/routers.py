from rest_framework_nested import routers

from . import views


router = routers.DefaultRouter()
router.register(r'pay/orders', views.OrderViewSet, base_name='pay-orders')
router.register(r'pay/refund', views.RefundViewSet, base_name='pay-refund')
