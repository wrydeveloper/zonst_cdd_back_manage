<template>
  <div v-loading="loading">
    <el-card>
      <el-row class="filter">
        <date-select style="display: inline-block;" type="date" @change="changeDate"></date-select>
        <el-button class="search-btn" type="primary" size="small" @click="handleSearch">查询</el-button>
      </el-row>
      <br />
      <el-table
        :data="pays"
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
          label="支付类型">
          <template slot-scope="scope">
            {{ scope.row.pay_type | filterPayType }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="srv_name"
          label="支付商户">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="总额">
          <template slot-scope="scope">
            {{ scope.row.total_money | filterMoney }}
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

import analysis from '../../api/analysis'
import DateSelect from '../../components/selects/DateSelect'
import { filterPayType, filterMoney } from '../../filters'

export default {
  data () {
    return {
      pays: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      params: {},
      dateRange: ''
    }
  },
  created () {
    this.init(this.$route)
    this.list(this.params)
  },
  components: {
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
      analysis.listPay(params).then((data) => {
        this.pays = data.results
        this.total = data.count
        this.loading = false
      })
    },
    handleSearch () {
      this.currentPage = 1
      delete this.params.page
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'AnalysisPay', query: params })
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.params['page'] = val
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'AnalysisPay', query: params })
    }
  },
  filters: {
    filterPayType,
    filterMoney
  },
  watch: {
    $route: {
      deep: true,
      handler: function (val) {
        if (val.name === 'AnalysisPay') {
          this.init(val)
          this.list(this.params)
        }
      }
    }
  }
}
</script>
