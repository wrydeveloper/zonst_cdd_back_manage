<template>
  <div>
    <el-form class="change-password" :model="changePasswordForm" :rules="changePasswordRule" ref="changePasswordForm" label-width="100px">
      <el-form-item class="change-password-item" label="旧密码" prop="old_password">
        <el-input type="password" v-model="changePasswordForm.old_password" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item class="change-password-item" label="新密码" prop="new_password">
        <el-input type="password" v-model="changePasswordForm.new_password" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item class="change-password-item">
        <el-button type="primary" @click="submitForm('changePasswordForm')">确定</el-button>
        <el-button @click="resetForm('changePasswordForm')">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import account from '../api/account.js'

export default {
  name: 'ChangePassword',
  data () {
    return {
      changePasswordForm: {
        old_password: '',
        new_password: ''
      },
      changePasswordRule: {
        old_password: [
          { required: true, message: '请输入旧密码', trigger: 'blur' }
        ],
        new_password: [
          { required: true, message: '请输入新密码', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    submitForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          account.changePassword(this.changePasswordForm).then((data) => {
            this.$message({
              type: 'success',
              message: '修改成功!'
            })
            this.$refs[formName].resetFields()
          }).catch((error) => {
            this.$message({
              type: 'warning',
              message: error.message
            })
          })
        } else {
          return false
        }
      })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    }
  }
}
</script>

<style>
.change-password {
  width: 400px;
  margin: 0 auto;
  margin-top: 200px;
}
.change-password-item {
  margin-right: 100px;
}
</style>
