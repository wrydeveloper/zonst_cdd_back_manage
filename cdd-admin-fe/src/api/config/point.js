import api from '../../api'
import { API_ROOT } from '../../config'

const lottery = {
  list (params) {
    return api.get(`${API_ROOT}/api/points/`, {
      params: params
    })
  },
  retrieve (id) {
    return api.get(`${API_ROOT}/api/points/${id}/`)
  },
  create (data) {
    return api.post(`${API_ROOT}/api/points/`, data)
  },
  update (id, data) {
    return api.patch(`${API_ROOT}/api/points/${id}/`, data)
  },
  destory (id) {
    return api.delete(`${API_ROOT}/api/points/${id}/`)
  }
}

export default lottery
