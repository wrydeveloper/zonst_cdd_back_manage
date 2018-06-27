<template>
  <div v-loading="loading">
    <el-card>
      <el-row class="filter">
        <el-col :span="9">
          <date-select style="display: inline-block;" @change="changeDate"></date-select>
          <number-lottery-alias-select @change="changeLotteryAlias"></number-lottery-alias-select>
          <el-button class="search-btn" type="primary" size="small" @click="handleSearch">查询</el-button>
        </el-col>
        <el-col :span="15">
          <div class="statistic-label">中奖汇总：<span class="statistic">{{ statistic.bonus_money | filterMoney }}</span></div>
        </el-col>
      </el-row>
      <br />
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
          prop="play_type"
          label="玩法">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="是否大奖">
          <template slot-scope="scope">
            {{ scope.row.is_bomb_bonus | filterIsBigAward }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="ticket_id"
          label="票号"
          width="200">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="单注奖金">
          <template slot-scope="scope">
            {{ scope.row.per_money | filterMoney }}
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
          prop="size"
          label="中奖注数">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="bonus_level"
          label="中奖等级">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="状态">
          <template slot-scope="scope">
            <el-tag
              size="mini"
              :type="handleStatusTagType(scope.row.status)">{{ scope.row.status | filterLotteryBonusStatus }}
            </el-tag>
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
import { filterLotteryBonusStatus, filterNumberLotteryType, filterIsBigAward, filterMoney } from '../../filters'

export default {
  data () {
    return {
      loading: false,
      bonus: [],
      statistic: {
        bonus_money: 0
      },
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
      number.listBonus(params).then((data) => {
        this.bonus = data.results.data
        this.statistic = data.results.statistic
        this.total = data.count
        this.loading = false
      })
    },
    handleSearch () {
      this.currentPage = 1
      delete this.params.page
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'NumberBonus', query: params })
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
      this.$router.push({ name: 'NumberBonus', query: params })
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
    filterLotteryBonusStatus,
    filterNumberLotteryType,
    filterIsBigAward,
    filterMoney
  },
  watch: {
    $route: {
      deep: true,
      handler: function (val) {
        if (val.name === 'NumberBonus') {
          this.init(val)
          this.list(this.params)
        }
      }
    }
  }
}
</script>
