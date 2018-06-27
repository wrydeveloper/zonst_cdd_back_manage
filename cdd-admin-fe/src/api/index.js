import axios from 'axios'

import router from '../router'
import { API_ROOT } from '../config'
import user from '../localStorage/user'

const api = axios.create({
  baseURL: API_ROOT
})

// 接口请求前
api.interceptors.request.use(function (request) {
  if (router.currentRoute.name === 'Login') {
    return request
  }
  // 是否已授权，是否有token
  if (user.IsAuthenticated()) {
    // 若有token，拼装Authorization Header
    request.headers.common['Authorization'] = `Bearer ${user.token}`
    return request
  }
  return request
})

// 接口响应后
api.interceptors.response.use(function (response) {
  return response.data
}, function (error) {
  if (error.response.status === 403) {
    user.logout()
    router.push({ name: 'Login' })
  } else if (error.response.status === 401) {
    user.logout()
    router.push({ name: 'Login' })
  } else {
    return Promise.reject(error.response.data)
  }
})

export default api
