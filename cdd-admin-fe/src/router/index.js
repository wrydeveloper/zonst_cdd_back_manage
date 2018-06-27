import Vue from 'vue'
import Router from 'vue-router'

import user from '../localStorage/user'

import Login from '@/views/Login'
import Logout from '@/views/Logout'
import Layout from '@/views/Layout'
import ChangePassword from '@/views/ChangePassword'
import Home from '@/views/Home'
import User from '@/views/User'
import PromotionCommerce from '@/views/promotion/Commerce'
import PromotionProxy from '@/views/promotion/Proxy'
import PromotionChannel from '@/views/promotion/Channel'
import PeriodThirdparty from '@/views/number/PeriodThirdparty'
import PeriodLocal from '@/views/number/PeriodLocal'
import NumberBonus from '@/views/number/Bonus'
import FinanceRecharge from '@/views/finance/Recharge'
import FinanceWithdraw from '@/views/finance/Withdraw'
import OrderNumber from '@/views/order/Number'
import OrderNumberFollow from '@/views/order/NumberFollow'
import OrderSports from '@/views/order/Sports'
import PayOrder from '@/views/pay/Order'
import PayRefund from '@/views/pay/Refund'
import AnalysisChannel from '@/views/analysis/Channel'
import AnalysisProxy from '@/views/analysis/Proxy'
import AnalysisUser from '@/views/analysis/User'
import AnalysisBetNumber from '@/views/analysis/BetNumber'
import AnalysisBetSports from '@/views/analysis/BetSports'
import AnalysisPay from '@/views/analysis/Pay'
import SearchNumber from '@/views/search/Number'
import SearchSports from '@/views/search/Sports'
import ConfigLottery from '@/views/config/Lottery'
import ConfigMerchant from '@/views/config/Merchant'
import ConfigChannel from '@/views/config/Channel'
import ConfigPoint from '@/views/config/Point'
import ConfigBanner from '@/views/config/Banner'
import ConfigApk from '@/views/config/Apk'
import SportMatch from '@/views/sport/Match'
import SportBouns from '@/views/sport/Bouns'
import NoPermission from '@/views/NoPermission'
import Role from '@/views/permission/Role'
import Admin from '@/views/permission/Admin'

Vue.use(Router)

const routes = [
  {
    path: '/',
    component: Layout,
    children: [
      {
        path: '/',
        name: 'Home',
        component: Home,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/user',
        name: 'User',
        component: User,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/promotion/commerce',
        name: 'PromotionCommerce',
        component: PromotionCommerce,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/promotion/proxy',
        name: 'PromotionProxy',
        component: PromotionProxy,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/promotion/channel',
        name: 'PromotionChannel',
        component: PromotionChannel,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/number/period/thirdparty',
        name: 'PeriodThirdparty',
        component: PeriodThirdparty,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/number/period/local',
        name: 'PeriodLocal',
        component: PeriodLocal,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/number/bonus',
        name: 'NumberBonus',
        component: NumberBonus,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/finance/recharge',
        name: 'FinanceRecharge',
        component: FinanceRecharge,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/finance/withdraw',
        name: 'FinanceWithdraw',
        component: FinanceWithdraw,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/order/number',
        name: 'OrderNumber',
        component: OrderNumber,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/order/number/follow',
        name: 'OrderNumberFollow',
        component: OrderNumberFollow,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/order/sports',
        name: 'OrderSports',
        component: OrderSports,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/pay/order',
        name: 'PayOrder',
        component: PayOrder,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/pay/refund',
        name: 'PayRefund',
        component: PayRefund,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/analysis/channel',
        name: 'AnalysisChannel',
        component: AnalysisChannel,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/analysis/proxy',
        name: 'AnalysisProxy',
        component: AnalysisProxy,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/analysis/user',
        name: 'AnalysisUser',
        component: AnalysisUser,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/analysis/bet/number',
        name: 'AnalysisBetNumber',
        component: AnalysisBetNumber,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/analysis/bet/sports',
        name: 'AnalysisBetSports',
        component: AnalysisBetSports,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/analysis/pay',
        name: 'AnalysisPay',
        component: AnalysisPay,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/search/number',
        name: 'SearchNumber',
        component: SearchNumber,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/search/sports',
        name: 'SearchSports',
        component: SearchSports,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/config/lottery',
        name: 'ConfigLottery',
        component: ConfigLottery,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/config/pay/merchant',
        name: 'ConfigMerchant',
        component: ConfigMerchant,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/config/pay/channel',
        name: 'ConfigChannel',
        component: ConfigChannel,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/config/point',
        name: 'ConfigPoint',
        component: ConfigPoint,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/config/banner',
        name: 'ConfigBanner',
        component: ConfigBanner
      },
      {
        path: '/config/apk',
        name: 'ConfigApk',
        component: ConfigApk
      },
      {
        path: '/password/change',
        name: 'ChangePassword',
        component: ChangePassword,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/sport/match',
        name: 'SportMatch',
        component: SportMatch,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/sport/bouns',
        name: 'SportBouns',
        component: SportBouns,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/role',
        name: 'Role',
        component: Role,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/admin',
        name: 'Admin',
        component: Admin,
        meta: {
          requiresAuth: true
        }
      }
    ],
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/logout',
    name: 'Logout',
    component: Logout
  },
  {
    path: '/nopermission',
    name: 'NoPermission',
    component: NoPermission
  }
]

const router = new Router({
  routes: routes,
  mode: 'history'
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!user.IsAuthenticated()) {
      next({
        path: '/login'
      })
    }
  }
  next()
})

export default router
