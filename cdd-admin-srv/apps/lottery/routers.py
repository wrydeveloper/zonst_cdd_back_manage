from rest_framework_nested import routers

from . import views


router = routers.DefaultRouter()
router.register(r'number/periods/thirdparty', views.NumberPeriodThirdpartyViewSet, base_name='number-periods-thirdparty')
router.register(r'number/periods/local', views.NumberPeriodLocalViewSet, base_name='number-periods-local')
router.register(r'number/bonus', views.NumberLotteryBonusViewSet, base_name='number-bonus')
router.register(r'sports/match', views.SportsLotteryMatchViewSet, base_name='sports-match')  # 竞彩赛事
router.register(r'sports/bouns', views.SportsLotteryBonusViewSet, base_name='sports-bouns')  # 中奖信息
