<template>
  <div v-loading="loading">
    <el-card>
      <el-row class="filter">
        <el-col :span="16">
          <el-input style="width: 400px;"
            size="small"
            placeholder="支持用户ID、订单ID及手机号码查询"
            v-model="keyword"
            @change="changeKeyword"
            clearable>
          </el-input>
          <date-select style="display: inline-block;" @change="changeDate"></date-select>
          <el-select v-model="status" placeholder="状态" size="small" clearable @change="changeStatus">
            <el-option
              v-for="item in status_option_list"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
          <el-button class="search-btn" type="primary" size="small" @click="handleSearch">查询</el-button>
        </el-col>
        <el-col :span="8">
          <div class="statistic-label">金额汇总：<span class="statistic">{{ statistic.total_money | filterMoney }}</span></div>
        </el-col>
      </el-row>
      <br />
      <el-table
        :data="withdraws"
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
          label="订单ID"
          width="250">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="金额">
          <template slot-scope="scope">
            {{ scope.row.cash_money | filterMoney }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="状态">
          <template slot-scope="scope">
            <el-tag
              size="mini"
              :type="handleStatusTagType(scope.row.status)">{{ scope.row.status | filterWithdrawStatus }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="status_time"
          label="处理时间"
          width="180">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="req_time"
          label="申请时间"
          width="180">
        </el-table-column>
        <el-table-column
          label="操作"
          width="180"
          align="center"
          v-if="user.role === 'commerce'">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" v-if="scope.row.status === 0" @click="handleCheck(scope.row.id, 'check', scope.row.user_id)">
              审核
            </el-button>
            <el-button size="mini" v-else @click="handleCheck(scope.row.id, 'detail', scope.row.user_id)">
              明细
            </el-button>
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
      <user-bill-dialog @pass="handlePass" @reject="handleReject" ref="userBillDialog"></user-bill-dialog>
    </el-card>
  </div>
</template>

<script>
import finance from '../../api/finance'
import user from '../../localStorage/user'

import UserDetailDialog from '../../components/dialogs/UserDetailDialog'
import UserBillDialog from '../../components/dialogs/UserBillDialog'
import DateSelect from '../../components/selects/DateSelect'
import { filterWithdrawStatus, filterMoney } from '../../filters'

export default {
  data () {
    return {
      loading: false,
      user: {},
      withdraws: [],
      statistic: {
        total_money: 0
      },
      total: 0,
      currentPage: 1,
      pageSize: 10,
      params: {},
      keyword: '',
      dateRange: '',
      status: '',
      status_option_list: [
        {
          label: '待处理 ',
          value: '0'
        },
        {
          label: '已成功 ',
          value: '1'
        },
        {
          label: '已失败 ',
          value: '2'
        },
        {
          label: '已审核',
          value: '3'
        }
      ]
    }
  },
  created () {
    this.user = user
    this.init(this.$route)
    this.list(this.params)
  },
  components: {
    UserDetailDialog,
    UserBillDialog,
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
      if (route.query.status) {
        this.params['status'] = route.query.status
        this.status = route.query.status
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
      finance.listWithdraw(params).then((data) => {
        this.withdraws = data.results.data
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
      this.$router.push({ name: 'FinanceWithdraw', query: params })
    },
    handleCheck (id, type, userID) {
      let params = {
        user_id: userID
      }
      this.$refs.userBillDialog.show(id, type, params)
    },
    handlePass (val) {
      finance.passWithdraw(val).then((data) => {
        this.$message({
          type: 'success',
          message: '处理成功!'
        })
        this.list(this.params)
      }).catch((error) => {
        this.$message({
          type: 'warning',
          message: error.message
        })
      })
    },
    handleReject (val) {
      finance.rejectWithdraw(val).then((data) => {
        this.$message({
          type: 'success',
          message: '处理成功!'
        })
        this.list(this.params)
      }).catch((error) => {
        this.$message({
          type: 'warning',
          message: error.message
        })
      })
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
    changeStatus (val) {
      if (val) {
        this.status = val
        this.params['status'] = val
      } else {
        this.status = ''
        delete this.params.status
      }
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.params['page'] = val
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'FinanceWithdraw', query: params })
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
    filterWithdrawStatus,
    filterMoney
  },
  watch: {
    $route: {
      deep: true,
      handler: function (val) {
        if (val.name === 'FinanceWithdraw') {
          this.init(val)
          this.list(this.params)
        }
      }
    }
  }
}
</script>

<style>
.filter {
  text-align: left;
}
.search-btn {
  margin-left: 20px;
}
</style>
