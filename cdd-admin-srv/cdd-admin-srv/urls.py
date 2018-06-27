from django.conf.urls import include, url

from apps.account.routers import router as account_router
from apps.user.routers import router as user_router
from apps.promotion.routers import router as promotion_router
from apps.lottery.routers import router as lottery_router
from apps.finance.routers import router as finance_router
from apps.order.routers import router as order_router
from apps.pay.routers import router as pay_router
from apps.analysis.routers import router as analysis_router
from apps.config.routers import router as config_router
from apps.event.routers import router as event_router
from apps.search.views import SearchResultView
from apps.upload.views import UploadView
from apps.analysis.views import ChartUserView
from apps.analysis.views import ChartSportsView
from apps.analysis.views import ChartNumberView
from apps.analysis.views import ChartSalesTrendView
from apps.analysis.views import ChartSalesRankView
from apps.analysis.views import ChartUserH5TransformView
from apps.analysis.views import ChartUserMobileTransformView
from apps.analysis.views import ChartSalesScaleView
from apps.admin.routers import router as admin_router

from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

from rest_framework.permissions import AllowAny
schema_view = get_schema_view(title='TEST API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer], permission_classes=(AllowAny,))

urlpatterns = [
    url(r'^docs/', schema_view),
    url(r'^api/', include(account_router.urls)),
    url(r'^api/', include(user_router.urls)),
    url(r'^api/', include(promotion_router.urls)),
    url(r'^api/', include(lottery_router.urls)),
    url(r'^api/', include(finance_router.urls)),
    url(r'^api/', include(order_router.urls)),
    url(r'^api/', include(pay_router.urls)),
    url(r'^api/', include(analysis_router.urls)),
    url(r'^api/', include(event_router.urls)),
    url(r'^api/config/', include(config_router.urls)),
    url(r'^api/search/', SearchResultView.as_view()),
    url(r'^api/upload/', UploadView.as_view()),
    url(r'^api/analysis/chart/user/', ChartUserView.as_view()),
    url(r'^api/analysis/chart/sports/', ChartSportsView.as_view()),
    url(r'^api/analysis/chart/number/', ChartNumberView.as_view()),
    url(r'^api/analysis/chart/sales/trend/', ChartSalesTrendView.as_view()),
    url(r'^api/analysis/chart/sales/rank/', ChartSalesRankView.as_view()),
    url(r'^api/analysis/chart/transform/h5/', ChartUserH5TransformView.as_view()),
    url(r'^api/analysis/chart/transform/mobile/', ChartUserMobileTransformView.as_view()),
    url(r'^api/analysis/chart/sales/scale/', ChartSalesScaleView.as_view()),
    url(r'^api/', include(admin_router.urls)),
    url(r'^api-auth/$', include('rest_framework.urls', namespace='rest_framework'))
]
