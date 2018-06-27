<template>
  <div v-loading="loading">
    <el-card>
      <el-row class="filter">
        <date-select style="display: inline-block;" @change="changeDate"></date-select>
        <number-lottery-alias-select @change="changeLotteryAlias"></number-lottery-alias-select>
        <el-button class="search-btn" type="primary" size="small" @click="handleSearch">查询</el-button>
      </el-row>
      <br />
      <el-table
        :data="periods"
        style="width: 100%">
        <el-table-column
          header-align="center"
          type="index"
          width="80">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="lottery_name"
          label="彩票名称">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="lottery_period"
          label="彩期">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="start_time"
          label="开始时间">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="stop_time"
          label="结束时间">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="official_start_time"
          label="官方开始时间">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="official_stop_time"
          label="官方结束时间">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="bonus_code"
          label="开奖号码">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="销售金额">
          <template slot-scope="scope">
            {{ scope.row.sales_money | filterMoney }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="中奖金额">
          <template slot-scope="scope">
            {{ scope.row.bonus_money | filterMoney }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="状态">
          <template slot-scope="scope">
            {{ scope.row.status | filterNumberLotteryPeriodStatus }}
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
import { format } from 'date-fns'

import number from '../../api/number'

import NumberLotteryAliasSelect from '../../components/selects/NumberLotteryAliasSelect'
import DateSelect from '../../components/selects/DateSelect'
import { filterNumberLotteryPeriodStatus, filterMoney } from '../../filters'

export default {
  data () {
    return {
      loading: false,
      periods: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      params: {},
      dateRange: '',
      officialDateRange: '',
      lottery_alias: ''
    }
  },
  created () {
    this.init(this.$route)
    this.list(this.params)
  },
  components: {
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
      let officialStartTime = null
      let officialStopTime = null
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
      if (route.query.official_start_time) {
        this.params['official_start_time'] = route.query.official_start_time
        officialStartTime = new Date(route.query.official_start_time)
      }
      if (route.query.official_stop_time) {
        this.params['official_stop_time'] = route.query.official_stop_time
        officialStopTime = new Date(route.query.official_stop_time)
      }
      if (officialStartTime && officialStopTime) {
        this.officialDateRange = [officialStartTime, officialStopTime]
      }
      this.total = this.currentPage * 10
    },
    list (params) {
      this.loading = true
      number.listPeriodThirdparty(params).then((data) => {
        this.periods = data.results
        this.total = data.count
        this.loading = false
      })
    },
    handleSearch () {
      this.currentPage = 1
      delete this.params.page
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'PeriodThirdparty', query: params })
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
    handleCurrentChange (val) {
      this.currentPage = val
      this.params['page'] = val
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'PeriodThirdparty', query: params })
    },
    handleDatePickChange (val) {
      if (val) {
        this.params['start_time'] = format(this.dateRange[0], 'YYYY-MM-DD 00:00:00')
        this.params['stop_time'] = format(this.dateRange[1], 'YYYY-MM-DD 23:59:59')
      } else {
        delete this.params.start_time
        delete this.params.stop_time
      }
    },
    handleOfficialDatePickChange (val) {
      if (val) {
        this.params['official_start_time'] = format(this.officialDateRange[0], 'YYYY-MM-DD 00:00:00')
        this.params['official_stop_time'] = format(this.officialDateRange[1], 'YYYY-MM-DD 23:59:59')
      } else {
        delete this.params.official_start_time
        delete this.params.official_stop_time
      }
    }
  },
  filters: {
    filterNumberLotteryPeriodStatus,
    filterMoney
  },
  watch: {
    $route: {
      deep: true,
      handler: function (val) {
        if (val.name === 'PeriodThirdparty') {
          this.init(val)
          this.list(this.params)
        }
      }
    }
  }
}
</script>
