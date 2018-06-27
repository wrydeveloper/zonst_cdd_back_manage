<template>
  <div>
    <el-dialog
      title="用户信息"
      width="25%"
      :visible.sync="visible">
      <el-form :model="form" label-width="120px">
        <el-form-item class="wrap" label="姓名：">
          {{ form.real_name }}
        </el-form-item>
        <el-form-item class="wrap" label="昵称：">
          {{ form.nick_name }}
        </el-form-item>
        <el-form-item class="wrap" label="手机：">
          {{ form.phone_number }}
        </el-form-item>
        <el-form-item class="wrap" label="所属代理：">
          {{ form.proxy_name }}
        </el-form-item>
        <el-form-item class="wrap" label="所属商务：">
          {{ form.bd_name }}
        </el-form-item>
        <el-form-item class="wrap" label="身份证：">
          {{ form.id_card }}
        </el-form-item>
        <el-form-item class="wrap" label="银行卡：">
          {{ form.bank_card }}
        </el-form-item>
        <el-form-item class="wrap" label="银行名：">
          {{ form.bank_name }}
        </el-form-item>
        <el-form-item class="wrap" label="开户行：">
          {{ form.bank_addr }}
        </el-form-item>
        <el-form-item class="wrap" label="最后登录时间：">
          {{ form.last_login_time }}
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="visible = false">关 闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import user from '../../api/user'

export default {
  data () {
    return {
      visible: false,
      form: {
        'real_name': '',
        'nick_name': '',
        'phone_number': '',
        'proxy_name': '',
        'bd_name': '',
        'id_card': '',
        'bank_card': '',
        'last_login_time': ''
      }
    }
  },
  methods: {
    show (id) {
      user.retrieve(id).then((data) => {
        this.visible = true
        this.form = data
      })
    }
  }
}
</script>

<style>
.wrap {
  text-align: left;
  word-wrap: break-word;
}
</style>
