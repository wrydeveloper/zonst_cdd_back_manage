<template>
  <div>
    <el-dialog
      title="用户钱包流水"
      :visible.sync="visible">
      <el-table
        :data="bills"
        border
        style="width: 100%">
        <el-table-column
          header-align="center"
          type="index"
          width="80">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="变更前余额">
          <template slot-scope="scope">
            {{ scope.row.balance_before | filterMoney }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="当前余额">
          <template slot-scope="scope">
            {{ scope.row.balance_now | filterMoney }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="交易金额">
          <template slot-scope="scope">
            {{ scope.row.fee | filterMoney }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="类型">
          <template slot-scope="scope">
            {{ scope.row.type | filterBillType }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="mark"
          label="备注">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="add_time"
          label="时间"
          width="180">
        </el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer" v-if="type === 'check'">
        <el-button type="primary" @click="pass">通过</el-button>
        <el-button @click="reject">不通过</el-button>
      </div>
      <div slot="footer" class="dialog-footer" v-else>
        <el-button @click="visible = false">关 闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import finance from '../../api/finance'

export default {
  data () {
    return {
      id: null,
      type: '',
      visible: false,
      bills: []
    }
  },
  methods: {
    show (id, type, params) {
      this.id = id
      this.type = type
      finance.listBill(params).then((data) => {
        this.visible = true
        this.bills = data.results
      })
    },
    pass () {
      this.visible = false
      this.$emit('pass', this.id)
    },
    reject () {
      this.visible = false
      this.$emit('reject', this.id)
    }
  },
  filters: {
    filterBillType (val) {
      let dictBillType = {
        0: '未知',
        1: '投注消费',
        2: '中奖',
        3: '提现',
        4: '充值',
        5: '出票失败退款'
      }
      return dictBillType[val]
    },
    filterMoney (val) {
      return '￥' + val / 100
    }
  }
}
</script>
