<template>
  <div>
    <el-dialog
      title="渠道信息"
      width="25%"
      :visible.sync="visible">
      <el-form :model="form" label-width="120px">
        <el-form-item class="wrap" label="姓名：">
          {{ form.real_name }}
        </el-form-item>
        <el-form-item class="wrap" label="手机：">
          {{ form.phone }}
        </el-form-item>
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
        <el-form-item class="wrap" label="CPS比例：">
          {{ form.commission }}
        </el-form-item>
        <el-form-item class="wrap" label="备注：">
          {{ form.mark }}
        </el-form-item>
        <el-form-item class="wrap" label="创建时间：">
          {{ form.add_time }}
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="visible = false">关 闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import channel from '../../api/channel'

export default {
  data () {
    return {
      visible: false,
      form: {
        'real_name': '',
        'phone': '',
        'promotion_url': '',
        'h5_url': '',
        'android_url': '',
        'ios_url': '',
        'commission': '',
        'mark': ''
      }
    }
  },
  methods: {
    show (id) {
      channel.retrieve(id).then((data) => {
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
