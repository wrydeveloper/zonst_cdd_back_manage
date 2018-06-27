<template>
  <div v-loading="loading">
    <el-card>
      <el-row class="filter">
        <el-col :span="15">
          <date-select style="display: inline-block;" type="date" @change="changeDate"></date-select>
          <el-select v-model="bd" placeholder="商务" size="small" clearable @change="changeBd">
            <el-option
              v-for="item in bd_option_list"
              :key="item.id"
              :label="item.bd_name"
              :value="item.id">
            </el-option>
          </el-select>
          <el-select v-model="proxy" placeholder="代理" size="small" clearable @change="changeProxy">
            <el-option
              v-for="item in proxy_option_list"
              :key="item.id"
              :label="item.proxy_name"
              :value="item.id">
            </el-option>
          </el-select>
          <channel-select @change="changeChannel"></channel-select>
          <platform-select @change="changePlatform"></platform-select>
          <el-button class="search-btn" type="primary" size="small" @click="handleSearch">查询</el-button>
        </el-col>
        <el-col :span="9">
          <div class="statistic-label">金额汇总：<span class="statistic">{{ statistic.cps_data | filterMoney }}</span></div>
        </el-col>
      </el-row>
      <br />
      <el-table
        :data="reports"
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
          prop="channel_id"
          label="渠道ID">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="proxy_name"
          label="代理">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="bd_name"
          label="商务">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="平台">
          <template slot-scope="scope">
            {{ scope.row.platform | filterPlatform }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="cpa_data"
          label="注册数量">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="消费金额">
          <template slot-scope="scope">
            {{ scope.row.cps_data | filterMoney }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="1日">
          <template slot-scope="scope">
            {{ scope.row.day1 | filterRate }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="3日">
          <template slot-scope="scope">
            {{ scope.row.day3 | filterRate }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="7日">
          <template slot-scope="scope">
            {{ scope.row.day7 | filterRate }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="15日">
          <template slot-scope="scope">
            {{ scope.row.day15 | filterRate }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="30日">
          <template slot-scope="scope">
            {{ scope.row.day30 | filterRate }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="60日">
          <template slot-scope="scope">
            {{ scope.row.day60 | filterRate }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="90日">
          <template slot-scope="scope">
            {{ scope.row.day90 | filterRate }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="arpu"
          label="ARPU">
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
import commerce from '../../api/commerce'
import proxy from '../../api/proxy'

import ChannelSelect from '../../components/selects/ChannelSelect'
import PlatformSelect from '../../components/selects/PlatformSelect'
import DateSelect from '../../components/selects/DateSelect'
import { filterPlatform, filterMoney, filterRate } from '../../filters'

export default {
  data () {
    return {
      loading: false,
      reports: [],
      statistic: {
        cps_data: 0
      },
      total: 0,
      currentPage: 1,
      pageSize: 10,
      params: {},
      dateRange: '',
      channel: '',
      proxy: '',
      proxy_option_list: [],
      bd: '',
      bd_option_list: [],
      platform: ''
    }
  },
  created () {
    this.init(this.$route)
    this.list(this.params)
    this.listBdOption()
    this.listProxyOption()
  },
  components: {
    ChannelSelect,
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
      if (route.query.bd) {
        this.params['bd'] = route.query.bd
        this.bd = parseInt(route.query.bd)
      }
      if (route.query.proxy) {
        this.params['proxy'] = route.query.proxy
        this.proxy = parseInt(route.query.proxy)
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
      analysis.listUser(params).then((data) => {
        this.reports = data.results.data
        this.statistic = data.results.statistic
        this.total = data.count
        this.loading = false
      })
    },
    listBdOption () {
      commerce.listOption().then((data) => {
        this.bd_option_list = data
      })
    },
    listProxyOption () {
      proxy.listOption().then((data) => {
        this.proxy_option_list = data
      })
    },
    handleSearch () {
      if (this.keyword !== '') {
        this.params['keyword'] = this.keyword
      }
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'AnalysisUser', query: params })
    },
    changeBd (val) {
      if (val) {
        this.bd = val
        this.params['bd'] = val
      } else {
        this.bd = ''
        delete this.params.bd
      }
    },
    changeChannel (val) {
      if (val) {
        this.channel = val
        this.params['channel'] = val
      } else {
        this.channel = ''
        delete this.params.channel
      }
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
      this.$router.push({ name: 'AnalysisUser', query: params })
    }
  },
  filters: {
    filterPlatform,
    filterMoney,
    filterRate
  },
  watch: {
    $route: {
      deep: true,
      handler: function (val) {
        if (val.name === 'AnalysisUser') {
          this.init(val)
          this.list(this.params)
        }
      }
    }
  }
}
</script>
