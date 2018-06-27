import api from '../api'
import { API_ROOT } from '../config'

const order = {
  listNumber (params) {
    return api.get(`${API_ROOT}/api/orders/number/`, {
      params: params
    })
  },
  listNumberFollow (params) {
    return api.get(`${API_ROOT}/api/number/follows/`, {
      params: params
    })
  },
  listSports (params) {
    return api.get(`${API_ROOT}/api/orders/sports/`, {
      params: params
    })
  },
  retrieveNumberDetail (id) {
    return api.get(`${API_ROOT}/api/orders/number/${id}/`)
  },
  retrieveSportsDetail (id) {
    return api.get(`${API_ROOT}/api/orders/sports/${id}/`)
  }
}

export default order
