import api from '../api'
import { API_ROOT } from '../config'

const account = {
  getToken (data) {
    return api.post(`${API_ROOT}/api/account/token/`, data)
  },
  getInformation () {
    return api.get(`${API_ROOT}/api/account/information/`)
  },
  changePassword (data) {
    return api.patch(`${API_ROOT}/api/account/password/`, data)
  }
}

export default account
