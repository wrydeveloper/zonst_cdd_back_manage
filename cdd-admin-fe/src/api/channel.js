import api from '../api'
import { API_ROOT } from '../config'

const channel = {
  list (params) {
    return api.get(`${API_ROOT}/api/channels/`, {
      params: params
    })
  },
  retrieve (id) {
    return api.get(`${API_ROOT}/api/channels/${id}/`)
  },
  create (data) {
    return api.post(`${API_ROOT}/api/channels/`, data)
  },
  update (id, data) {
    return api.patch(`${API_ROOT}/api/channels/${id}/`, data)
  },
  destory (id) {
    return api.delete(`${API_ROOT}/api/channels/${id}/`)
  },
  listOption () {
    return api.get(`${API_ROOT}/api/channels/options/`)
  }
}

export default channel
