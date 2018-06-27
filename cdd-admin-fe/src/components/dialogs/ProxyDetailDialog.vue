<template>
  <div>
    <el-dialog
      width="25%"
      :visible.sync="visible"
      :show-close="false"
      :close-on-press-escape="false"
      :close-on-click-modal="false">
      <div slot="title">
        代理信息
      </div>
      <el-form :model="form" label-width="120px">
        <el-form-item class="wrap" label="代理名称：">
          {{ form.proxy_name }}
        </el-form-item>
        <el-form-item class="wrap" label="公司名称：">
          {{ form.company_name }}
        </el-form-item>
        <el-form-item class="wrap" label="真实姓名：">
          {{ form.real_name }}
        </el-form-item>
        <el-form-item class="wrap" label="联系电话：">
          {{ form.phone }}
        </el-form-item>
        <el-form-item class="wrap" label="QQ：">
          {{ form.qq }}
        </el-form-item>
        <el-form-item class="wrap" label="代理等级：">
          {{ form.proxy_level | filterPromotionLevel }}
        </el-form-item>
        <el-form-item class="wrap" label="代理类型：">
          {{ form.proxy_type | filterPromotionType }}
        </el-form-item>
        <el-form-item class="wrap" label="比例/单价：">
          {{ form.commission }}
        </el-form-item>
        <el-form-item class="wrap" label="结算周期：">
          {{ form.pay_type | filterPromotionPayType }}
        </el-form-item>
        <el-form-item class="wrap" label="银行卡号：">
          {{ form.bank_number }}
        </el-form-item>
        <el-form-item class="wrap" label="开户姓名：">
          {{ form.bank_account }}
        </el-form-item>
        <el-form-item class="wrap" label="开户行：">
          {{ form.bank_name }}
        </el-form-item>
        <el-form-item class="wrap" label="支行地址：">
          {{ form.bank_addr }}
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="visible = false">关 闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import proxy from '../../api/proxy'

import { filterPromotionType, filterPromotionPayType, filterPromotionLevel } from '../../filters'

export default {
  data () {
    return {
      visible: false,
      form: {
        proxy_name: '',
        company_name: '',
        phone: '',
        qq: '',
        bd_id: '',
        proxy_level: '',
        proxy_type: '',
        commission: 0,
        pay_type: '',
        real_name: '',
        bank_account: '',
        bank_name: '',
        bank_number: '',
        bank_addr: ''
      }
    }
  },
  methods: {
    show (id) {
      proxy.retrieve(id).then((data) => {
        this.visible = true
        this.form = data
      })
    }
  },
  filters: {
    filterPromotionType,
    filterPromotionPayType,
    filterPromotionLevel
  }
}
</script>

<style>
.wrap {
  text-align: left;
  word-wrap: break-word;
}
</style>
