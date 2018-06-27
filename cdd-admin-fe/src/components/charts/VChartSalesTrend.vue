<template>
  <div class="sales-trend-box">
    <h4>销售额趋势</h4>
    <div id="sales-trend"></div>
  </div>
</template>

<script>
import chart from '../../api/chart'

import G2 from '@antv/g2'

export default {
  data () {
    return {
      chart: null,
      chart_data: []
    }
  },
  created () {
    chart.getSalesTrend().then((data) => {
      this.chart_data = data.chart_data
    })
  },
  methods: {
    drawChart: function (data) {
      this.chart = new G2.Chart({
        container: 'sales-trend',
        padding: [50, 50, 50, 100],
        width: 1100,
        height: 360,
        forceFit: true
      })
      this.chart.tooltip({
        inPlot: true,
        follow: true,
        showTitle: false,
        itemTpl: '<li>{title}: ￥{value}</li>'
      })
      this.chart.legend(false)
      this.chart.source(data)
      this.chart.interval().position('month*money')
      this.chart.render()
    }
  },
  watch: {
    chart_data: function (val) {
      this.drawChart(val)
    }
  }
}
</script>
