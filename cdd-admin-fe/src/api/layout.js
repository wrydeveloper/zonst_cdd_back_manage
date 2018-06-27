import api from '../api'
import { API_ROOT } from '../config'

const layout = {
  listLayout (params) {
    return api.get(`${API_ROOT}/api/menu/`, {
      params: params
    })
  }
}

export default layout
