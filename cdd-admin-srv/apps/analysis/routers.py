from rest_framework_nested import routers

from . import views


router = routers.DefaultRouter()
router.register(r'analysis/channel', views.ChannelDataDayViewSet, base_name='analysis-channel')
router.register(r'analysis/proxy', views.ProxyDataDayViewSet, base_name='analysis-proxy')
router.register(r'analysis/user', views.UserDataDayViewSet, base_name='analysis-user')
router.register(r'analysis/bet/number', views.NumberBetDataDayViewSet, base_name='analysis-bet-number')
router.register(r'analysis/bet/sports', views.SportsBetDataDayViewSet, base_name='analysis-bet-sports')
router.register(r'analysis/pay', views.PayDataDayViewSet, base_name='analysis-pay')
