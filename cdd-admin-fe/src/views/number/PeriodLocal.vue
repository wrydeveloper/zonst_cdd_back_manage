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
          label="彩种">
          <template slot-scope="scope">
            {{ scope.row.lottery_alias | filterNumberLotteryType }}
          </template>
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
          prop="weekday"
          label="星期">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="状态">
          <template slot-scope="scope">
            {{ scope.row.status | filterNumberLotteryPeriodStatus }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="add_time"
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
    </el-card>
  </div>
</template>

<script>
import number from '../../api/number'

import NumberLotteryAliasSelect from '../../components/selects/NumberLotteryAliasSelect'
import DateSelect from '../../components/selects/DateSelect'
import { filterNumberLotteryPeriodStatus, filterNumberLotteryType } from '../../filters'

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
      number.listPeriodLocal(params).then((data) => {
        this.periods = data.results
        this.total = data.count
        this.loading = false
      })
    },
    handleSearch () {
      this.currentPage = 1
      delete this.params.page
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'PeriodLocal', query: params })
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
      this.$router.push({ name: 'PeriodLocal', query: params })
    }
  },
  filters: {
    filterNumberLotteryPeriodStatus,
    filterNumberLotteryType
  },
  watch: {
    $route: {
      deep: true,
      handler: function (val) {
        if (val.name === 'PeriodLocal') {
          this.init(val)
          this.list(this.params)
        }
      }
    }
  }
}
</script>
