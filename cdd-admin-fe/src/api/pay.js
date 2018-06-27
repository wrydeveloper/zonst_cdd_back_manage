import api from '../api'
import { API_ROOT } from '../config'

const pay = {
  listOrder (params) {
    return api.get(`${API_ROOT}/api/pay/orders/`, {
      params: params
    })
  },
  listRefund (params) {
    return api.get(`${API_ROOT}/api/pay/refund/`, {
      params: params
    })
  }
}

export default pay
