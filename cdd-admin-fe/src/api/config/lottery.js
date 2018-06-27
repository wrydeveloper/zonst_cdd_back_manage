import api from '../../api'
import { API_ROOT } from '../../config'

const lottery = {
  list (params) {
    return api.get(`${API_ROOT}/api/config/lotteries/`, {
      params: params
    })
  },
  retrieve (id) {
    return api.get(`${API_ROOT}/api/config/lotteries/${id}/`)
  },
  create (data) {
    return api.post(`${API_ROOT}/api/config/lotteries/`, data)
  },
  update (id, data) {
    return api.patch(`${API_ROOT}/api/config/lotteries/${id}/`, data)
  },
  destory (id) {
    return api.delete(`${API_ROOT}/api/config/lotteries/${id}/`)
  }
}

export default lottery
