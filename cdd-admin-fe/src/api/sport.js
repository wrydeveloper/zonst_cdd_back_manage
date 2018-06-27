import api from '../api'
import {API_ROOT} from '../config'

const sport = {
  listMatch (params) {
    return api.get(`${API_ROOT}/api/sports/match/`, {
      params: params
    })
  },
  listBouns (params) {
    return api.get(`${API_ROOT}/api/sports/bouns/`, {
      params: params
    })
  }
}
export default sport
