import api from '../../api'
import { API_ROOT } from '../../config'

const banner = {
  list (params) {
    return api.get(`${API_ROOT}/api/config/banners/`, {
      params: params
    })
  },
  retrieve (id) {
    return api.get(`${API_ROOT}/api/config/banners/${id}/`)
  },
  create (data) {
    return api.post(`${API_ROOT}/api/config/banners/`, data)
  },
  update (id, data) {
    return api.patch(`${API_ROOT}/api/config/banners/${id}/`, data)
  },
  destory (id) {
    return api.delete(`${API_ROOT}/api/config/banners/${id}/`)
  }
}

export default banner
