import api from '../api'
import { API_ROOT } from '../config'

const role = {
  list (params) {
    return api.get(`${API_ROOT}/api/roles/`, {
      params: params
    })
  },
  retrieve (id) {
    return api.get(`${API_ROOT}/api/roles/${id}/`)
  },
  create (data) {
    return api.post(`${API_ROOT}/api/roles/`, data)
  },
  update (id, data) {
    return api.patch(`${API_ROOT}/api/roles/${id}/`, data)
  }
}

export default role
