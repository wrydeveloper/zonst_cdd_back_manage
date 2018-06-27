<template>
  <el-form class="login" :model="loginForm" :rules="loginRule" ref="loginForm" label-width="100px">
    <div class="titleName">
      {{ titileName }}
    </div>
    <el-form-item class="login-item" label="账号" prop="username">
      <el-input type="text" v-model="loginForm.username" auto-complete="off" clearable></el-input>
    </el-form-item>
    <el-form-item class="login-item" label="密码" prop="password">
      <el-input type="password" v-model="loginForm.password" auto-complete="off" clearable @keyup.enter.native="submitForm('loginForm')"></el-input>
    </el-form-item>
    <el-form-item class="login-item">
      <el-button class="login-btn" type="primary" :loading="loading" @click="submitForm('loginForm')">{{ btnLoginText }}</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import account from '../api/account'
import user from '../localStorage/user'

export default {
  name: 'Login',
  data () {
    return {
      loading: false,
      btnLoginText: '登录',
      loginForm: {
        username: '',
        password: ''
      },
      loginRule: {
        username: [
          { required: true, message: '请输入账号', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      },
      titileName: ''
    }
  },
  methods: {
    submitForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.loading = true
          this.btnLoginText = '登录中...'
          account.getToken(this.loginForm).then((data) => {
            user.login(data)
            if (user.role === 'commerce') {
              this.$router.push({ name: 'Home' })
            } else {
              this.$router.push({ name: 'User' })
            }
          }).catch((error) => {
            this.$message({
              type: 'warning',
              message: error.message
            })
            this.loading = false
            this.btnLoginText = '登录'
          })
        } else {
          return false
        }
      })
    }
  },
  created () {
    var title = window.location.href
    var reg1 = /^((http|https):\/\/)?admin(-test)?\.\w*\.cn\/login$/
    var reg2 = /^((http|https):\/\/)?corp(-test)?\.\w*\.cn\/login$/

    if (title.match(reg1)) {
      this.titileName = '管理后台'
    } else if (title.match(reg2)) {
      this.titileName = '代理后台'
    } else {
      this.titileName = '本地后台'
    }
  }
}
</script>

<style>
.login {
  width: 400px;
  margin: 0 auto;
  margin-top: 120px;
}
.login-item {
  margin-right: 100px;
}
.login-btn {
  width: 200px;
}
.titleName{
  font-size: 40px;
  margin-bottom: 40px;
}
</style>
