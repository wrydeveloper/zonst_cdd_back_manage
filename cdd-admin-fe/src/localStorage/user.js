const localStorage = global.localStorage

const USER_TOKEN = 'auth.token'
const USER_ROLE = 'auth.role'
const USER_LEVEL = 'auth.level'

class User {
  constructor () {
    this.token = localStorage.getItem(USER_TOKEN)
    this.role = localStorage.getItem(USER_ROLE)
    this.level = localStorage.getItem(USER_LEVEL)
  }

  IsAuthenticated () {
    if (!this.token || !this.role || !this.level) {
      return false
    }
    return true
  }

  login (data) {
    localStorage.setItem(USER_TOKEN, data.token)
    localStorage.setItem(USER_ROLE, data.role)
    localStorage.setItem(USER_LEVEL, data.level)
    this.token = data.token
    this.role = data.role
    this.level = data.level
  }

  logout () {
    localStorage.clear()
  }
}

const user = new User()

export default user
