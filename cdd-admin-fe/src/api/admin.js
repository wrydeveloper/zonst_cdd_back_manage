import api from '../api'
import { API_ROOT } from '../config'

const admin = {
  listRoleData (params) {
    return api.get(`${API_ROOT}/api/admin/rolemsg/`, {
      params: params
    })
  },
  retrieveRole (id) {
    return api.get(`${API_ROOT}/api/admin/rolemsg/${id}/`)
  },
  createRole (data) {
    return api.post(`${API_ROOT}/api/admin/rolemsg/`, data)
  },
  updateRole (id, data) {
    return api.patch(`${API_ROOT}/api/admin/rolemsg/${id}/`, data)
  },
  destoryRole (id) {
    return api.delete(`${API_ROOT}/api/admin/rolemsg/${id}/`)
  },
  listAllPermission (params) {
    return api.get(`${API_ROOT}/api/admin/allpermission/`, {
      params: params
    })
  },
  listRolePermission (id) {
    return api.get(`${API_ROOT}/api/admin/rolepermission/?id=${id}`)
  },
  updateRolePermission (data) {
    return api.post(`${API_ROOT}/api/admin/changerolepermission/`, data)
  },
  listAdminData (params) {
    return api.get(`${API_ROOT}/api/admins/`, {
      params: params
    })
  },
  updateAdminRoleSetting (id, data) {
    return api.patch(`${API_ROOT}/api/admins/${id}/`, data)
  }
}

export default admin
