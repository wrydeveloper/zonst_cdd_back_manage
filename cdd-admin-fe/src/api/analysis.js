import api from '../api'
import { API_ROOT } from '../config'

const analysis = {
  listChannel (params) {
    return api.get(`${API_ROOT}/api/analysis/channel/`, {
      params: params
    })
  },
  listProxy (params) {
    return api.get(`${API_ROOT}/api/analysis/proxy/`, {
      params: params
    })
  },
  listUser (params) {
    return api.get(`${API_ROOT}/api/analysis/user/`, {
      params: params
    })
  },
  listBetNumber (params) {
    return api.get(`${API_ROOT}/api/analysis/bet/number/`, {
      params: params
    })
  },
  listBetSports (params) {
    return api.get(`${API_ROOT}/api/analysis/bet/sports/`, {
      params: params
    })
  },
  listPay (params) {
    return api.get(`${API_ROOT}/api/analysis/pay/`, {
      params: params
    })
  }
}

export default analysis
