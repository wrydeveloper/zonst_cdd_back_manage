let API_ROOT

switch (process.env.NODE_ENV) {
  case 'production':
    API_ROOT = 'http://api-admin.duoduocp.cn'
    break
  case 'staging':
    API_ROOT = 'http://api-admin-test.duoduocp.cn'
    break
  case 'development':
    API_ROOT = 'http://127.0.0.1:8000'
    break
  default:
    API_ROOT = 'http://127.0.0.1:8000'
}

export {
  API_ROOT
}
