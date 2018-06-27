<template>
  <div class="sales-rank-box">
    <h4>渠道销售额排名
      <el-date-picker
        style="float: right;"
        size="mini"
        v-model="dateRange"
        type="daterange"
        align="right"
        unlink-panels
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        @change="handleDatePickChange">
      </el-date-picker>
    </h4>
    <ul class="rank-list">
      <li v-for="(item, index) in rank_list" :key="item.channel_id"><span v-bind:class="{ active: index < 3 }">{{ index + 1 }}</span><span>渠道 {{ item.channel_id }}</span><span>{{ item.cps | filterMoney }}</span></li>
    </ul>
  </div>
</template>

<script>
import { format } from 'date-fns'
import chart from '../../api/chart'

import { filterMoney } from '../../filters'

export default {
  data () {
    return {
      rank_list: [],
      dateRange: '',
      params: {}
    }
  },
  created () {
    chart.getSalesRank(this.params).then((data) => {
      this.rank_list = data
    })
  },
  methods: {
    handleDatePickChange (val) {
      if (val) {
        this.params['sdate'] = format(this.dateRange[0], 'YYYY-MM-DD')
        this.params['edate'] = format(this.dateRange[1], 'YYYY-MM-DD')
      } else {
        delete this.params.sdate
        delete this.params.edate
      }
      chart.getSalesRank(this.params).then((data) => {
        this.rank_list = data
      })
    }
  },
  filters: {
    filterMoney
  }
}
</script>

<style>
.sales-rank-box {
  padding: 0 0 32px 72px;
}
.sales-rank-box .rank-list {
  margin: 25px 0 0;
  padding: 0 32px 0 0;
  list-style: none;
}
.rank-list li {
  zoom: 1;
  margin-top: 16px;
  text-align: left;
}
.rank-list li span {
  color: rgba(0,0,0,.65);
  font-size: 14px;
  line-height: 22px;
}
.rank-list li span:first-child {
  background-color: #f5f5f5;
  border-radius: 20px;
  display: inline-block;
  font-size: 12px;
  font-weight: 600;
  margin-right: 24px;
  height: 20px;
  line-height: 20px;
  width: 20px;
  text-align: center;
}
.rank-list li span.active {
  background-color: #314659;
  color: #fff;
}
.rank-list li span:last-child {
  float: right;
}
</style>
