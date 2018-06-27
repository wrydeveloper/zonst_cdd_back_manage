<template>
  <div v-loading="loading">
    <el-card>
      <el-row class="filter">
        <el-col :span="18">
          <el-input style="width: 400px;"
            size="small"
            placeholder="支持用户ID、订单ID及手机号查询"
            v-model="keyword"
            @change="changeKeyword"
            clearable>
          </el-input>
          <date-select style="display: inline-block;" @change="changeDate"></date-select>
          <el-select v-model="pay_type" placeholder="充值方式" size="small" clearable @change="changePayType">
            <el-option
              v-for="item in pay_type_option_list"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
          <el-select v-model="pay_status" placeholder="状态" size="small" clearable @change="changePayStatus">
            <el-option
              v-for="item in pay_status_option_list"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
          <el-button class="search-btn" type="primary" size="small" @click="handleSearch">查询</el-button>
        </el-col>
        <el-col :span="6">
          <div class="statistic-label">金额汇总：<span class="statistic">{{ statistic.total_money | filterMoney }}</span></div>
        </el-col>
      </el-row>
      <br />
      <el-table
        :data="recharges"
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
          label="金额">
          <template slot-scope="scope">
            {{ scope.row.charge_money | filterMoney }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="充值方式">
          <template slot-scope="scope">
            {{ scope.row.pay_type | filterRechargePayType }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="状态">
          <template slot-scope="scope">
            <el-tag
              size="mini"
              :type="handleStatusTagType(scope.row.pay_status)">{{ scope.row.pay_status | filterRechargeStatus }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="order_time"
          label="创建时间"
          width="180">
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

import finance from '../../api/finance'

import UserDetailDialog from '../../components/dialogs/UserDetailDialog'
import DateSelect from '../../components/selects/DateSelect'
import { filterRechargeStatus, filterRechargePayType, filterMoney } from '../../filters'

export default {
  data () {
    return {
      loading: false,
      recharges: [],
      statistic: {
        total_money: 0
      },
      total: 0,
      currentPage: 1,
      pageSize: 10,
      params: {},
      keyword: '',
      dateRange: '',
      pay_type: '',
      pay_type_option_list: [
        {
          label: '余额',
          value: '0'
        },
        {
          label: '微信',
          value: '1'
        },
        {
          label: '支付宝',
          value: '2'
        },
        {
          label: '银行卡',
          value: '3'
        }
      ],
      pay_status: '',
      pay_status_option_list: [
        {
          label: '待支付',
          value: '0'
        },
        {
          label: '已成功',
          value: '1'
        }
      ]
    }
  },
  created () {
    this.init(this.$route)
    this.list(this.params)
  },
  components: {
    UserDetailDialog,
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
      if (route.query.pay_type) {
        this.params['pay_type'] = route.query.pay_type
        this.pay_type = route.query.pay_type
      }
      if (route.query.pay_status) {
        this.params['pay_status'] = route.query.pay_status
        this.pay_status = route.query.pay_status
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
      finance.listRecharge(params).then((data) => {
        this.recharges = data.results.data
        this.total = data.count
        this.statistic = data.results.statistic
        this.loading = false
      })
    },
    getUserDetail (userID) {
      this.$refs.userDetailDialog.show(userID)
    },
    handleSearch () {
      this.currentPage = 1
      delete this.params.page
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'FinanceRecharge', query: params })
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
    changePayType (val) {
      if (val) {
        this.pay_type = val
        this.params['pay_type'] = val
      } else {
        this.pay_type = ''
        delete this.params.pay_type
      }
    },
    changePayStatus (val) {
      if (val) {
        this.pay_status = val
        this.params['pay_status'] = val
      } else {
        this.pay_status = ''
        delete this.params.pay_status
      }
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.params['page'] = val
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'FinanceRecharge', query: params })
    },
    handleStatusTagType (val) {
      if (val === 1) {
        return 'success'
      } else {
        return 'danger'
      }
    }
  },
  filters: {
    filterRechargeStatus,
    filterRechargePayType,
    filterMoney
  },
  watch: {
    $route: {
      deep: true,
      handler: function (val) {
        if (val.name === 'FinanceRecharge') {
          this.init(val)
          this.list(this.params)
        }
      }
    }
  }
}
</script>
