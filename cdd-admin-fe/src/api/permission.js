import api from '../api'
import { API_ROOT } from '../config'

const role = {
  list (params) {
    return api.get(`${API_ROOT}/api/permissions/`, {
      params: params
    })
  }
}

export default role
