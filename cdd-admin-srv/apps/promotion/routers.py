from rest_framework_nested import routers

from . import views


router = routers.DefaultRouter()
router.register(r'commerces', views.CommerceViewSet, base_name='commerces')
router.register(r'proxies', views.ProxyViewSet, base_name='proxies')
router.register(r'channels', views.ChannelViewSet, base_name='channels')
