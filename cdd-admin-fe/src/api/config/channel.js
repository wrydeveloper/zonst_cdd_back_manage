import api from '../../api'
import { API_ROOT } from '../../config'

const channel = {
  list (params) {
    return api.get(`${API_ROOT}/api/config/pay/channels/`, {
      params: params
    })
  },
  retrieve (id) {
    return api.get(`${API_ROOT}/api/config/pay/channels/${id}/`)
  },
  create (data) {
    return api.post(`${API_ROOT}/api/config/pay/channels/`, data)
  },
  update (id, data) {
    return api.patch(`${API_ROOT}/api/config/pay/channels/${id}/`, data)
  },
  destory (id) {
    return api.delete(`${API_ROOT}/api/config/pay/channels/${id}/`)
  }
}

export default channel
