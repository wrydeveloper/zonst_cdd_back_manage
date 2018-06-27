<template>
  <div v-loading="loading">
    <el-card>
      <el-row class="filter">
        <el-col :span="20">
          <el-input style="width: 400px;"
            @change="changeKeyword"
            size="small"
            placeholder="支持用户ID、订单ID及手机号查询"
            v-model="keyword"
            clearable>
          </el-input>
          <date-select style="display: inline-block;" @change="changeDate"></date-select>
          <number-lottery-alias-select @change="changeLotteryAlias"></number-lottery-alias-select>
          <el-select v-model="order_status" placeholder="订单状态" size="small" clearable @change="changeOrderStatus">
            <el-option
              v-for="item in order_status_option_list"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
          <el-select v-model="follow_status" placeholder="追号状态" size="small" clearable @change="changeFollowStatus">
            <el-option
              v-for="item in follow_status_option_list"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
          <el-button class="search-btn" type="primary" size="small" @click="handleSearch">查询</el-button>
        </el-col>
        <el-col :span="4">
          <div class="statistic-label">金额汇总：<span class="statistic">{{ statistic.total_money | filterMoney }}</span></div>
        </el-col>
      </el-row>
      <br />
      <el-table
        :data="follows"
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
          width="200"
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
          label="倍数">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="投注金额">
          <template slot-scope="scope">
            {{ scope.row.total_money | filterMoney }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="follow_num"
          label="追号期数">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="follow_remain_num"
          label="剩余期数">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="追号状态">
          <template slot-scope="scope">
            {{ scope.row.follow_status | filterFollowStatus }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="订单状态">
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
            <el-button size="mini" @click="goOrder(scope.row.order_id)">追号列表</el-button>
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
    </el-card>
  </div>
</template>

<script>
import user from '../../localStorage/user'
import order from '../../api/order'

import UserDetailDialog from '../../components/dialogs/UserDetailDialog'
import NumberLotteryAliasSelect from '../../components/selects/NumberLotteryAliasSelect'
import DateSelect from '../../components/selects/DateSelect'
import { filterOrderStatus, filterFollowStatus, filterMoney, filterNumberLotteryType } from '../../filters'

export default {
  data () {
    return {
      loading: false,
      user: {},
      follows: [],
      statistic: {
        total_money: 0
      },
      total: 0,
      currentPage: 1,
      pageSize: 10,
      params: {},
      keyword: '',
      dateRange: '',
      userFormVisable: false,
      userForm: {},
      lottery_alias: '',
      order_status: '',
      order_status_option_list: [
        {
          label: '待支付',
          value: '0'
        },
        {
          label: '支付成功',
          value: '1'
        }
      ],
      follow_status: '',
      follow_status_option_list: [
        {
          label: '停止追号',
          value: '0'
        },
        {
          label: '正常追号',
          value: '1'
        },
        {
          label: '完成追号',
          value: '2'
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
    NumberLotteryAliasSelect,
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
      if (route.query.keyword) {
        this.params['keyword'] = route.query.keyword
        this.keyword = route.query.keyword
      }
      if (route.query.order_status) {
        this.params['order_status'] = route.query.order_status
        this.order_status = route.query.order_status
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
      order.listNumberFollow(params).then((data) => {
        this.follows = data.results.data
        this.statistic = data.results.statistic
        this.total = data.count
        this.loading = false
      })
    },
    handleSearch () {
      this.currentPage = 1
      delete this.params.page
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'OrderNumberFollow', query: params })
    },
    getUserDetail (userID) {
      this.$refs.userDetailDialog.show(userID)
    },
    goOrder (id) {
      let query = {
        keyword: id
      }
      this.$router.push({ name: 'OrderNumber', query: query })
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
    changeFollowStatus (val) {
      if (val) {
        this.follow_status = val
        this.params['follow_status'] = val
      } else {
        this.follow_status = ''
        delete this.params.follow_status
      }
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.params['page'] = val
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'OrderNumberFollow', query: params })
    }
  },
  filters: {
    filterFollowStatus,
    filterOrderStatus,
    filterNumberLotteryType,
    filterMoney
  },
  watch: {
    $route: {
      deep: true,
      handler: function (val) {
        if (val.name === 'OrderNumberFollow') {
          this.init(val)
          this.list(this.params)
        }
      }
    }
  }
}
</script>
