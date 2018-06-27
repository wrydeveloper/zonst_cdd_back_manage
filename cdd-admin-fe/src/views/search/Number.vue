<template>
  <div v-loading="loading">
    <el-card>
      <el-table
        :data="orders"
        :row-class-name="tableRowClassName"
        style="width: 100%">
        <el-table-column
          header-align="center"
          type="index"
          width="80">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="用户ID">
          <template slot-scope="scope">
            <a @click="getUserDetail(scope.row.user_id)">
              {{ scope.row.user_id }}
            </a>
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="order_id"
          label="订单ID">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="彩种">
          <template slot-scope="scope">
            {{ scope.row.lottery_alias | filterNumberLotteryType }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="amount"
          label="倍数"
          width="80">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="投注金额"
          width="80">
          <template slot-scope="scope">
            <el-button v-if="scope.row.order_status !== 6"
              @click.native.prevent="getOrderDetail(scope.row.order_pk)"
              type="text"
              size="medium">
              {{ scope.row.total_money | filterMoney }}
            </el-button>
            <div v-else>
              {{ scope.row.total_money | filterMoney }}
            </div>
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="中奖金额"
          width="80">
          <template slot-scope="scope">
            <el-button v-if="scope.row.order_status === 6"
              @click.native.prevent="getOrderDetail(scope.row.order_pk)"
              type="text"
              size="medium">
              {{ scope.row.bonus_money | filterMoney }}
            </el-button>
            <div v-else>
              {{ scope.row.bonus_money | filterMoney }}
            </div>
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="状态">
          <template slot-scope="scope">
            {{ scope.row.order_status | filterOrderStatus }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="order_time"
          label="创建时间"
          width="180">
        </el-table-column>
        <el-table-column
          label="操作"
          width="180"
          align="center">
          <template slot-scope="scope">
            <el-button size="mini" v-if="scope.row.is_followed_order" @click="goFollow(scope.row.followed_order_id)">追号原单</el-button>
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
      <user-detail-dialog ref="userDetailDialog"></user-detail-dialog>
      <number-order-detail-dialog ref="numberOrderDetailDialog"></number-order-detail-dialog>
    </el-card>
  </div>
</template>

<script>
import search from '../../api/search'

import UserDetailDialog from '../../components/dialogs/UserDetailDialog'
import NumberOrderDetailDialog from '../../components/dialogs/NumberOrderDetailDialog'

import { filterOrderStatus, filterNumberLotteryType, filterMoney } from '../../filters'

export default {
  data () {
    return {
      loading: false,
      orders: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      params: {},
      keyword: ''
    }
  },
  created () {
    this.init(this.$route)
    this.list(this.params)
  },
  components: {
    UserDetailDialog,
    NumberOrderDetailDialog
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
      if (route.query.keyword) {
        this.params['keyword'] = route.query.keyword
        this.keyword = route.query.keyword
      }
      this.total = this.currentPage * 10
    },
    list (params) {
      this.loading = true
      search.list(params, 'number').then((data) => {
        this.orders = data.data
        this.total = data.count
        this.loading = false
      })
    },
    getUserDetail (userID) {
      this.$refs.userDetailDialog.show(userID)
    },
    getOrderDetail (orderID) {
      this.$refs.numberOrderDetailDialog.show(orderID)
    },
    goFollow (id) {
      let query = {
        keyword: id
      }
      this.$router.push({ name: 'OrderNumberFollow', query: query })
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.params['page'] = val
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'SearchNumber', query: params })
    },
    tableRowClassName ({row, rowIndex}) {
      if (row.order_status === 6) {
        return 'warning-row'
      }
    }
  },
  filters: {
    filterOrderStatus,
    filterNumberLotteryType,
    filterMoney
  },
  watch: {
    $route: {
      deep: true,
      handler: function (val) {
        if (val.name === 'SearchNumber') {
          this.init(val)
          this.list(this.params)
        }
      }
    }
  }
}
</script>
