import api from '../../api'
import { API_ROOT } from '../../config'

const merchant = {
  list (params) {
    return api.get(`${API_ROOT}/api/config/pay/merchants/`, {
      params: params
    })
  },
  retrieve (id) {
    return api.get(`${API_ROOT}/api/config/pay/merchants/${id}/`)
  },
  create (data) {
    return api.post(`${API_ROOT}/api/config/pay/merchants/`, data)
  },
  update (id, data) {
    return api.patch(`${API_ROOT}/api/config/pay/merchants/${id}/`, data)
  },
  destory (id) {
    return api.delete(`${API_ROOT}/api/config/pay/merchants/${id}/`)
  }
}

export default merchant
