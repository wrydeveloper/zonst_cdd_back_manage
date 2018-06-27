import api from '../api'
import { API_ROOT } from '../config'

const search = {
  list (params, lottery) {
    let _params = Object.assign({}, params)
    _params.lottery = lottery
    return api.get(`${API_ROOT}/api/search/${lottery}/`, {
      params: _params
    })
  }
}

export default search
