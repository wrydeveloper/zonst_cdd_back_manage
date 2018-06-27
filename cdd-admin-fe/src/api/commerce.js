import api from '../api'
import { API_ROOT } from '../config'

const commerce = {
  list (params) {
    return api.get(`${API_ROOT}/api/commerces/`, {
      params: params
    })
  },
  retrieve (id) {
    return api.get(`${API_ROOT}/api/commerces/${id}/`)
  },
  create (data) {
    return api.post(`${API_ROOT}/api/commerces/`, data)
  },
  update (id, data) {
    return api.patch(`${API_ROOT}/api/commerces/${id}/`, data)
  },
  destory (id) {
    return api.delete(`${API_ROOT}/api/commerces/${id}/`)
  },
  listOption () {
    return api.get(`${API_ROOT}/api/commerces/options/`)
  }
}

export default commerce
