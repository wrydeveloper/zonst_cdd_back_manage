from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register(r'banners', views.BannerViewSet, base_name='banners')
router.register(r'lotteries', views.LotteryViewSet, base_name='lotteries')
router.register(r'pay/merchants', views.PayMerchantViewSet, base_name='pay-merchants')
router.register(r'pay/channels', views.PayChannelViewSet, base_name='pay-channels')
router.register(r'bootpages', views.BootPageViewSet, base_name='bootpages')
