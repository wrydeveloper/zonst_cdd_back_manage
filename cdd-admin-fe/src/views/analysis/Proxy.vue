<template>
  <div v-loading="loading">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card>购彩汇总 <span class="statistic-span">{{ statistic.cps_data | filterMoney }}</span></el-card>
      </el-col>
      <el-col :span="6">
        <el-card>充值汇总 <span class="statistic-span">{{ statistic.charge_money | filterMoney }}</span></el-card>
      </el-col>
      <el-col :span="6">
        <el-card v-if="user.role === 'proxy'">我的佣金 <span class="statistic-span">{{ statistic.proxy_fee | filterMoney }}</span></el-card>
        <el-card v-else>成本汇总 <span class="statistic-span">{{ statistic.proxy_fee | filterMoney }}</span></el-card>
      </el-col>
      <el-col :span="6">
        <el-card>活动汇总 <span class="statistic-span">{{ statistic.coupon_fee | filterMoney }}</span></el-card>
      </el-col>
    </el-row>
    <br>
    <el-card>
      <el-row class="filter">
        <date-select style="display: inline-block;" type="date" @change="changeDate"></date-select>
        <proxy-select v-if="user.role !== 'proxy'" @change="changeProxy"></proxy-select>
        <platform-select @change="changePlatform"></platform-select>
        <el-button class="search-btn" type="primary" size="small" @click="handleSearch">查询</el-button>
      </el-row>
      <br />
      <el-table
        :data="orders"
        style="width: 100%">
        <el-table-column
          header-align="center"
          type="index"
          width="80">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="report_date"
          label="日期"
          width="180">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="proxy_name"
          label="代理名称"
          v-if="user.role !== 'proxy'">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="平台">
          <template slot-scope="scope">
            {{ scope.row.platform | filterPlatform }}
          </template>
        </el-table-column>
        <el-table-column v-if="user.role === 'commerce'"
          header-align="center"
          prop="cpc_data"
          label="下载量">
        </el-table-column>
        <el-table-column v-if="user.role === 'commerce'"
          header-align="center"
          prop="cpd_data"
          label="安装量">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="cpa_data"
          label="注册量">
        </el-table-column>
        <el-table-column v-if="user.role === 'commerce'"
          header-align="center"
          prop="order_count"
          label="订单量">
        </el-table-column>
        <el-table-column v-if="user.role === 'commerce'"
          header-align="center"
          prop="pay_user"
          label="付费人次">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="购彩金额">
          <template slot-scope="scope">
            {{ scope.row.cps_data | filterMoney }}
          </template>
        </el-table-column>
        <el-table-column v-if="user.role === 'commerce'"
          header-align="center"
          label="充值金额">
          <template slot-scope="scope">
            {{ scope.row.charge_money | filterMoney }}
          </template>
        </el-table-column>
        <el-table-column v-if="user.role === 'commerce'"
          header-align="center"
          label="代理成本">
          <template slot-scope="scope">
            {{ scope.row.proxy_fee | filterMoney }}
          </template>
        </el-table-column>
        <el-table-column v-if="user.role === 'proxy'"
          header-align="center"
          label="我的佣金">
          <template slot-scope="scope">
            {{ scope.row.proxy_fee | filterMoney }}
          </template>
        </el-table-column>
        <el-table-column v-if="user.role === 'commerce'"
          header-align="center"
          label="活动成本">
          <template slot-scope="scope">
            {{ scope.row.coupon_fee | filterMoney }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="cps_rate"
          label="分成比例">
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

import analysis from '../../api/analysis'
import user from '../../localStorage/user'

import ProxySelect from '../../components/selects/ProxySelect'
import PlatformSelect from '../../components/selects/PlatformSelect'
import DateSelect from '../../components/selects/DateSelect'

import { filterPlatform, filterMoney } from '../../filters'

export default {
  data () {
    return {
      loading: false,
      user: {},
      orders: [],
      statistic: {
        'cps_data': 0,
        'charge_money': 0,
        'proxy_fee': 0,
        'coupon_fee': 0
      },
      total: 0,
      currentPage: 1,
      pageSize: 10,
      params: {},
      dateRange: '',
      channel: '',
      platform: ''
    }
  },
  created () {
    this.user = user
    this.init(this.$route)
    this.list(this.params)
  },
  components: {
    ProxySelect,
    PlatformSelect,
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
      analysis.listProxy(params).then((data) => {
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
      this.$router.push({ name: 'AnalysisProxy', query: params })
    },
    changeProxy (val) {
      if (val) {
        this.proxy = val
        this.params['proxy'] = val
      } else {
        this.proxy = ''
        delete this.params.proxy
      }
    },
    changePlatform (val) {
      if (val) {
        this.platform = val
        this.params['platform'] = val
      } else {
        this.platform = ''
        delete this.params.platform
      }
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.params['page'] = val
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'AnalysisProxy', query: params })
    }
  },
  filters: {
    filterPlatform,
    filterMoney
  },
  watch: {
    $route: {
      deep: true,
      handler: function (val) {
        if (val.name === 'AnalysisProxy') {
          this.init(val)
          this.list(this.params)
        }
      }
    }
  }
}
</script>

<style>
.float-right {
  float: right;
}
</style>
