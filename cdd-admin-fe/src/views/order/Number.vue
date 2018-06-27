<template>
  <div v-loading="loading">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card>订单数 <span class="statistic-span">{{ statistic.total_count }}</span></el-card>
      </el-col>
      <el-col :span="8">
        <el-card>投注金额 <span class="statistic-span">{{ statistic.total_money | filterMoney }}</span></el-card>
      </el-col>
      <el-col :span="8">
        <el-card>中奖金额 <span class="statistic-span">{{ statistic.bonus_money | filterMoney }}</span></el-card>
      </el-col>
    </el-row>
    <br>
    <el-card>
      <el-row class="filter">
        <el-input style="width: 400px"
          @change="changeKeyword"
          size="small"
          placeholder="支持用户ID、订单ID、追号原单ID及手机号查询"
          v-model="keyword"
          clearable>
        </el-input>
        <date-select style="display: inline-block;" @change="changeDate"></date-select>
        <number-lottery-alias-select @change="changeLotteryAlias"></number-lottery-alias-select>
        <el-select v-model="is_followed_order" placeholder="是否追号" size="small" clearable @change="changeIsFollowedOrder">
          <el-option
            v-for="item in is_followed_order_option_list"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
        <lottery-order-status-select @change="changeOrderStatus"></lottery-order-status-select>
        <el-button class="search-btn" type="primary" size="small" @click="handleSearch">查询</el-button>
      </el-row>
      <br />
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
            <a v-if="user.role !== 'channel'" @click="getUserDetail(scope.row.user_id)">
              {{ scope.row.user_id }}
            </a>
            <div v-else>
              {{ scope.row.user_id }}
            </div>
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
              @click.native.prevent="getOrderDetail(scope.row.id)"
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
              @click.native.prevent="getOrderDetail(scope.row.id)"
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
import user from '../../localStorage/user'
import order from '../../api/order'

import UserDetailDialog from '../../components/dialogs/UserDetailDialog'
import NumberOrderDetailDialog from '../../components/dialogs/NumberOrderDetailDialog'
import NumberLotteryAliasSelect from '../../components/selects/NumberLotteryAliasSelect'
import LotteryOrderStatusSelect from '../../components/selects/LotteryOrderStatusSelect'
import DateSelect from '../../components/selects/DateSelect'
import { filterNumberLotteryType, filterOrderStatus, filterMoney } from '../../filters'

export default {
  data () {
    return {
      loading: false,
      user: {},
      orders: [],
      statistic: {
        total_count: 0,
        total_money: 0,
        bonus_money: 0
      },
      total: 0,
      currentPage: 1,
      pageSize: 10,
      params: {},
      keyword: '',
      dateRange: '',
      lottery_alias: '',
      order_status: '',
      is_followed_order: '',
      is_followed_order_option_list: [
        {
          label: '否',
          value: '0'
        },
        {
          label: '是',
          value: '1'
        }
      ]
    }
  },
  created () {
    this.init(this.$route)
    this.list(this.params)
    this.user = user
  },
  components: {
    UserDetailDialog,
    NumberOrderDetailDialog,
    NumberLotteryAliasSelect,
    LotteryOrderStatusSelect,
    DateSelect
  },
  methods: {
    changeDate (start, end) {
      if (start && end) {
        this.params['start_time'] = start
        this.params['stop_time'] = end
      } else {
        delete this.params.start_time
        delete this.params.stop_time
      }
    },
    init (route) {
      let startTime = null
      let stopTime = null
      if (route.query.pageSize) {
        this.params['page_size'] = route.query.pageSize
      }
      if (route.query.page) {
        this.params['page'] = route.query.page
        this.currentPage = parseInt(route.query.page)
      }
      if (route.query.is_followed_order) {
        this.params['is_followed_order'] = route.query.is_followed_order
        this.is_followed_order = route.query.is_followed_order
      }
      if (route.query.keyword) {
        this.params['keyword'] = route.query.keyword
        this.keyword = route.query.keyword
      }
      if (route.query.start_time) {
        this.params['start_time'] = route.query.start_time
        startTime = new Date(route.query.start_time)
      }
      if (route.query.stop_time) {
        this.params['stop_time'] = route.query.stop_time
        stopTime = new Date(route.query.stop_time)
      }
      if (startTime && stopTime) {
        this.dateRange = [startTime, stopTime]
      }
      this.total = this.currentPage * 10
    },
    list (params) {
      this.loading = true
      order.listNumber(params).then((data) => {
        this.orders = data.results.data
        this.total = data.count
        this.statistic = data.results.statistic
        this.loading = false
      })
    },
    handleSearch () {
      this.currentPage = 1
      delete this.params.page
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'OrderNumber', query: params })
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
    changeKeyword (val) {
      if (val) {
        this.keyword = val
        this.params['keyword'] = val
      } else {
        this.keyword = ''
        delete this.params.keyword
      }
    },
    changeLotteryAlias (val) {
      if (val) {
        this.lottery_alias = val
        this.params['lottery_alias'] = val
      } else {
        this.lottery_alias = ''
        delete this.params.lottery_alias
      }
    },
    changeOrderStatus (val) {
      if (val) {
        this.order_status = val
        this.params['order_status'] = val
      } else {
        this.order_status = ''
        delete this.params.order_status
      }
    },
    changeIsFollowedOrder (val) {
      if (val) {
        this.is_followed_order = val
        this.params['is_followed_order'] = val
      } else {
        this.is_followed_order = ''
        delete this.params.is_followed_order
      }
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.params['page'] = val
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'OrderNumber', query: params })
    },
    handleStatusTagType (val) {
      if (val === 1) {
        return 'success'
      } else {
        return 'danger'
      }
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
        if (val.name === 'OrderNumber') {
          this.init(val)
          this.list(this.params)
        }
      }
    }
  }
}
</script>
