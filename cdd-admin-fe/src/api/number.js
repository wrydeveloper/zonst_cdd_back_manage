import api from '../api'
import { API_ROOT } from '../config'

const number = {
  listPeriodThirdparty (params) {
    return api.get(`${API_ROOT}/api/number/periods/thirdparty/`, {
      params: params
    })
  },
  listPeriodLocal (params) {
    return api.get(`${API_ROOT}/api/number/periods/local/`, {
      params: params
    })
  },
  listBonus (params) {
    return api.get(`${API_ROOT}/api/number/bonus/`, {
      params: params
    })
  }
}

export default number
