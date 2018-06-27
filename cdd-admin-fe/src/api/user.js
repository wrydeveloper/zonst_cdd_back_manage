import api from '../api'
import { API_ROOT } from '../config'

const user = {
  list (params) {
    return api.get(`${API_ROOT}/api/users/`, {
      params: params
    })
  },
  retrieve (id) {
    return api.get(`${API_ROOT}/api/users/${id}/`)
  },
  changeChannel (id, data) {
    return api.patch(`${API_ROOT}/api/users/${id}/channel/`, data)
  }
}

export default user
