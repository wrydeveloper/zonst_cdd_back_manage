<template>
  <div v-loading="loading">
    <el-card>
      <el-table
        :data="refund"
        style="width: 100%">
        <el-table-column
          header-align="center"
          type="index"
          width="80">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="out_trade_no"
          label="订单ID">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="pay_type"
          label="支付类型">
          <template slot-scope="scope">
            {{ scope.row.pay_type | filterPayType }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="total_fee"
          label="总金额">
          <template slot-scope="scope">
            {{ scope.row.total_fee | filterMoney }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="status"
          label="状态">
          <template slot-scope="scope">
            {{ scope.row.status | filterPayStatus }}
          </template>
        </el-table-column>
      </el-table>
      <br>
      <el-row type="flex" justify="center">
        <el-pagination
          background
          layout="prev, pager, next"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-size="pageSize"
          :total="total">
        </el-pagination>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import pay from '../../api/pay'

import { filterPayType, filterPayStatus, filterMoney } from '../../filters'

export default {
  data () {
    return {
      loading: false,
      refund: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      params: {}
    }
  },
  created () {
    this.init(this.$route)
    this.list(this.params)
  },
  methods: {
    init (route) {
      if (route.query.pageSize) {
        this.params['page_size'] = route.query.pageSize
      }
      if (route.query.page) {
        this.params['page'] = route.query.page
        this.currentPage = parseInt(route.query.page)
      }
      this.total = this.currentPage * 10
    },
    list (params) {
      this.loading = true
      pay.listRefund(params).then((data) => {
        this.refund = data.results
        this.total = data.count
        this.loading = false
      })
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.params['page'] = val
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'PayRefund', query: params })
    }
  },
  filters: {
    filterPayType,
    filterPayStatus,
    filterMoney
  },
  watch: {
    $route: {
      deep: true,
      handler: function (val) {
        if (val.name === 'PayRefund') {
          this.init(val)
          this.list(this.params)
        }
      }
    }
  }
}
</script>
