<template>
  <div v-loading="loading">
    <el-card>
      <el-row class="filter">
        <el-col :span="15">
          <el-input style="width: 400px;"
            size="small"
            placeholder="支持场次编号、方案编号查询"
            v-model="keyword"
            @change="changeKeyword"
            clearable>
          </el-input>
         <date-select style="display: inline-block;" @change="changeDate"></date-select>
          <el-select v-model="is_big_award" size="small" placeholder="是否大奖" clearable @change="changeIsBigAward">
            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
          <el-button class="search-btn" type="primary" size="small" @click="handleSearch">查询</el-button>
        </el-col>
        <el-col :span="9">
          <div class="statistic-label">中奖汇总：<span class="statistic">{{ statistic.bonus_money | filterMoney }}</span></div>
          <div class="statistic-label">税后汇总：<span class="statistic">{{ statistic.win_money | filterMoney }}</span></div>
        </el-col>
      </el-row>
      <br/>
      <el-table
        :data="bonus"
        style="width: 100%">
        <el-table-column
          header-align="center"
          type="index"
          width="80">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="比赛类型">
          <template slot-scope="scope">
            {{ scope.row.game | filterSportsLotteryType }}
          </template>
        </el-table-column>
        <el-table-column
          label="场次"
          header-align='center'>
          <template slot-scope="scope">
            {{ scope.row.match_number | filterMatchNumber }}
          </template>
        </el-table-column>
        <el-table-column
          header-align='center'
          label="方案号"
          width="200">
          <template slot-scope="scope">
            {{ scope.row.scheme_id }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="是否大奖">
          <template slot-scope="scope">
            {{ scope.row.is_big_award | filterIsBigAward }}
          </template>
        </el-table-column>
        <el-table-column
          header-align='center'
          label="等级奖额">
          <template slot-scope="scope">
            {{ scope.row.level_money | filterMoney }}
          </template>
        </el-table-column>
        <el-table-column
          header-align='center'
          label="税后奖额">
          <template slot-scope="scope">
            {{ scope.row.win_money | filterMoney }}
          </template>
        </el-table-column>
        <el-table-column
          header-align='center'
          label="中奖注数">
          <template slot-scope="scope">
            {{ scope.row.prize_times }}
          </template>
        </el-table-column>
        <el-table-column
          header-align='center'
          label="中奖总金额">
          <template slot-scope="scope">
            {{ scope.row.bonus_money | filterMoney }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="返奖状态">
          <template slot-scope="scope">
            {{ scope.row.status | filterStatus }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="入库日期">
          <template slot-scope="scope">
            {{ scope.row.bonus_date }}
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
import { filterSportsLotteryType, filterIsBigAward, filterMoney } from '../../filters'

export default {
  data () {
    return {
      loading: false,
      bonus: [],
      statistic: {
        bonus_money: 0,
        win_money: 0
      },
      total: 0,
      currentPage: 1,
      pageSize: 10,
      params: {},
      dateRange: '',
      keyword: '',
      options: [
        {
          value: '1',
          label: '是'
        },
        {
          value: '0',
          label: '否'
        }
      ],
      is_big_award: ''
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
      if (route.query.keyword) {
        this.params['keyword'] = route.query.keyword
        this.keyword = route.query.keyword
      }
      this.total = this.currentPage * 10
    },
    list (params) {
      this.loading = true
      sport.listBouns(params).then((data) => {
        this.bonus = data.results.data
        this.statistic = data.results.statistic
        this.total = data.count
        this.loading = false
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
    changeIsBigAward (val) {
      if (val) {
        this.is_big_award = val
        this.params['is_big_award'] = val
      } else {
        this.is_big_award = ''
        delete this.params.is_big_award
      }
    },
    handleSearch () {
      this.currentPage = 1
      delete this.params.page
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'SportBouns', query: params })
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.params['page'] = val
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'SportBouns', query: params })
    }
  },
  filters: {
    filterSportsLotteryType,
    filterIsBigAward,
    filterMoney,
    filterMatchNumber (val) {
      let listMatchNumber = val.split('*')
      let dictWeek = {
        '1': '周一',
        '2': '周二',
        '3': '周三',
        '4': '周四',
        '5': '周五',
        '6': '周六',
        '7': '周日'
      }
      return dictWeek[listMatchNumber[1]] + listMatchNumber[2]
    },
    filterStatus (val) {
      let getStatus = {
        0: '未返奖',
        1: '已返奖'
      }
      return getStatus[val]
    }
  },
  watch: {
    $route: {
      deep: true,
      handler: function (val) {
        if (val.name === 'SportBouns') {
          this.init(val)
          this.list(this.params)
        }
      }
    }
  }
}
</script>
