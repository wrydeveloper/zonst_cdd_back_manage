import api from '../api'
import { API_ROOT } from '../config'

const chart = {
  getUser () {
    return api.get(`${API_ROOT}/api/analysis/chart/user/`)
  },
  getSports () {
    return api.get(`${API_ROOT}/api/analysis/chart/sports/`)
  },
  getNumber () {
    return api.get(`${API_ROOT}/api/analysis/chart/number/`)
  },
  getSalesTrend () {
    return api.get(`${API_ROOT}/api/analysis/chart/sales/trend/`)
  },
  getSalesRank (params) {
    return api.get(`${API_ROOT}/api/analysis/chart/sales/rank/`, {
      params: params
    })
  },
  getUserH5Transform (params) {
    return api.get(`${API_ROOT}/api/analysis/chart/transform/h5/`, {
      params: params
    })
  },
  getUserMobileTransform (params) {
    return api.get(`${API_ROOT}/api/analysis/chart/transform/mobile/`, {
      params: params
    })
  },
  getSalesScale (params) {
    return api.get(`${API_ROOT}/api/analysis/chart/sales/scale/`, {
      params: params
    })
  }
}

export default chart
