<template>
  <div v-loading="loading">
    <el-card>
      <el-row class="filter">
        <date-select style="display: inline-block;" @change="changeDate"></date-select>
        <el-button class="search-btn" type="primary" size="small" @click="handleSearch">查询</el-button>
      </el-row>
      <br/>
      <el-table
        :data="matches"
        style="width: 100%">
        <el-table-column
          header-align="center"
          type="index"
          width="80">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="主队">
          <template slot-scope="scope">
            {{ scope.row.home_team }}
          </template>
        </el-table-column>
        <el-table-column
          width="100"
          header-align="center"
          type="index"
          label="客队">
          <template slot-scope="scope">
            {{ scope.row.away_team }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="比赛时间">
          <template slot-scope="scope">
            {{ scope.row.match_time }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="截止时间">
          <template slot-scope="scope">
            {{ scope.row.end_time }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="比赛状态">
          <template slot-scope="scope">
            {{ scope.row.match_status | filterMatchStatus }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="添加时间">
          <template slot-scope="scope">
            {{scope.row.add_time }}
          </template>
        </el-table-column>
      </el-table>
      <br/>
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

import sport from '../../api/sport'
import DateSelect from '../../components/selects/DateSelect'
export default {
  data () {
    return {
      loading: false,
      matches: [],
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
      sport.listMatch(params).then((data) => {
        this.matches = data.results
        this.total = data.count
        this.loading = false
      })
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.params['page'] = val
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'SportMatch', query: params })
    },
    handleSearch () {
      this.currentPage = 1
      delete this.params.page
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'SportMatch', query: params })
    }
  },
  filters: {
    filterMatchStatus (val) {
      let getStatus = {
        0: '停售',
        1: '销售中',
        2: '比赛结束',
        3: '已返奖'
      }
      return getStatus[val]
    }
  },
  watch: {
    $route: {
      deep: true,
      handler: function (val) {
        if (val.name === 'SportMatch') {
          this.init(val)
          this.list(this.params)
        }
      }
    }
  }
}
</script>
