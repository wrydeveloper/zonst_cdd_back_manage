import api from '../api'
import { API_ROOT } from '../config'

const proxy = {
  list (params) {
    return api.get(`${API_ROOT}/api/proxies/`, {
      params: params
    })
  },
  retrieve (id) {
    return api.get(`${API_ROOT}/api/proxies/${id}/`)
  },
  create (data) {
    return api.post(`${API_ROOT}/api/proxies/`, data)
  },
  update (id, data) {
    return api.patch(`${API_ROOT}/api/proxies/${id}/`, data)
  },
  destory (id) {
    return api.delete(`${API_ROOT}/api/proxies/${id}/`)
  },
  listOption () {
    return api.get(`${API_ROOT}/api/proxies/options/`)
  }
}

export default proxy
