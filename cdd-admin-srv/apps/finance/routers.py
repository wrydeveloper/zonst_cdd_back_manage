from rest_framework_nested import routers

from . import views


router = routers.DefaultRouter()
router.register(r'recharges', views.RechargeViewSet, base_name='recharges')
router.register(r'withdraws', views.WithdrawViewSet, base_name='withdraws')
router.register(r'bills', views.BillViewSet, base_name='bills')
