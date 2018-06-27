<template>
  <el-card class="card">
    <div class="card-header">
      <div class="meta">
        <div class="analysis-label">今日数字彩投注总额</div>
        <div class="analysis-total">{{ total_money | filterMoney }}</div>
      </div>
      <div class="platform">
        H5
        <span>{{ h5_money | filterMoney }}</span>
        Android
        <span>{{ android_money | filterMoney }}</span>
        iOS
        <span>{{ ios_money | filterMoney }}</span>
      </div>
    </div>
    <div class="card-content">
      <div id="number"></div>
    </div>
    <div class="card-footer">
      今日订单数
      <span>{{ order_count }}</span>
      下单人次
      <span>{{ user_count }}</span>
    </div>
  </el-card>
</template>

<script>
import chart from '../../api/chart'
import {
  filterMoney
} from '../../filters'

import G2 from '@antv/g2'

export default {
  data () {
    return {
      chart: null,
      total_money: 0,
      h5_money: 0,
      android_money: 0,
      ios_money: 0,
      user_count: 0,
      order_count: 0,
      chart_data: []
    }
  },
  created () {
    chart.getNumber().then((data) => {
      this.total_money = data.total_money
      this.h5_money = data.h5_money
      this.android_money = data.android_money
      this.ios_money = data.ios_money
      this.user_count = data.user_count
      this.order_count = data.order_count
      this.chart_data = data.chart_data
      // console.log(this.chart_data, 'this.chart_data')
    })
  },
  methods: {
    drawChart: function (data) {
      this.chart = new G2.Chart({
        container: 'number',
        padding: [10, 10, 0, 10],
        forceFit: true,
        width: 550,
        height: 44
      })
      this.chart.axis('date', {
        line: null,
        label: null,
        tickLine: null
      })
      this.chart.axis('money', {
        label: null,
        grid: null
      })
      this.chart.tooltip({
        inPlot: true,
        follow: true,
        showTitle: false,
        itemTpl: '<li>{title}: ￥{value}</li>'
      })
      this.chart.legend(false)
      this.chart.source(data)
      this.chart.interval().position('date*money')
      this.chart.render()
    }
  },
  filters: {
    filterMoney
  },
  watch: {
    chart_data: function (val) {
      this.drawChart(val)
    }
  }
}

</script>
