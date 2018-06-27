<template>
  <div>
    <el-dialog
      title="修改用户信息"
      width="30%"
      :visible.sync="visible">
      <el-form :model="form" ref="form">
        <el-form-item label="渠道号">
          <el-input v-model="form.channel" placeholder="请输入渠道" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="银行卡号">
          <el-input v-model="form.bank_card" placeholder="请输入银行卡号" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="银行名">
          <el-input v-model="form.bank_name" placeholder="请输入银行名" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="开户行">
          <el-input v-model="form.bank_addr" placeholder="请输入开户行" auto-complete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="resetForm('form')">取 消</el-button>
        <el-button type="primary" @click="submitForm('form')">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import user from '../../api/user'

export default {
  data () {
    return {
      form: {},
      rule: {},
      visible: false
    }
  },
  methods: {
    show (id) {
      user.retrieve(id).then((data) => {
        this.visible = true
        this.form = data
      })
    },
    submitForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$confirm('此操作将更新用户信息, 是否继续?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            user.changeChannel(this.form.id, this.form).then((data) => {
              this.visible = false
              this.$message({
                type: 'success',
                message: '修改成功!'
              })
              this.$emit('confirm', this.start_time, this.stop_time)
            })
          })
        }
      })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
      this.visible = false
    }
  }
}
</script>
