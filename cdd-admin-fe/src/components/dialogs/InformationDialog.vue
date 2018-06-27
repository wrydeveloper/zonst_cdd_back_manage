<template>
  <div>
    <el-dialog
      title="推广链接"
      width="30%"
      :visible.sync="visible">
      <el-form :model="form" label-width="120px">
        <el-form-item class="wrap" label="推广链接：">
          {{ form.promotion_url }}
        </el-form-item>
        <el-form-item class="wrap" label="H5链接：">
          {{ form.h5_url }}
        </el-form-item>
        <el-form-item class="wrap" label="Android链接：">
          {{ form.android_url }}
        </el-form-item>
        <el-form-item class="wrap" label="iOS链接：">
          {{ form.ios_url }}
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="visible = false">关 闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import account from '../../api/account'

export default {
  data () {
    return {
      visible: false,
      form: {
        'promotion_url': '',
        'h5_url': '',
        'android_url': '',
        'ios_url': ''
      }
    }
  },
  methods: {
    show (id) {
      account.getInformation().then((data) => {
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
