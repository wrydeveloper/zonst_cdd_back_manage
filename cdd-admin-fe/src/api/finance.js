import api from '../api'
import { API_ROOT } from '../config'

const finance = {
  listRecharge (params) {
    return api.get(`${API_ROOT}/api/recharges/`, {
      params: params
    })
  },
  listWithdraw (params) {
    return api.get(`${API_ROOT}/api/withdraws/`, {
      params: params
    })
  },
  passWithdraw (id) {
    return api.get(`${API_ROOT}/api/withdraws/${id}/pass/`)
  },
  rejectWithdraw (id) {
    return api.get(`${API_ROOT}/api/withdraws/${id}/reject/`)
  },
  listBill (params) {
    return api.get(`${API_ROOT}/api/bills/`, {
      params: params
    })
  }
}

export default finance
