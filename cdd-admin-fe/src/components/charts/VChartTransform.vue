<template>
  <el-card>
    <h4>用户转化
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
    <el-row>
      <el-col :span="12">
        <h5>H5</h5>
        <div id="h5-transform"></div>
      </el-col>
      <el-col :span="12">
        <h5>移动端</h5>
        <div id="mobile-transform"></div>
      </el-col>
    </el-row>
  </el-card>
</template>

<script>
import { format } from 'date-fns'
import chart from '../../api/chart'

import G2 from '@antv/g2'

export default {
  data () {
    return {
      h5_chart: null,
      mobile_chart: null,
      h5_chart_data: [],
      mobile_chart_data: [],
      params: {},
      dateRange: ''
    }
  },
  created () {
    chart.getUserH5Transform(this.params).then((data) => {
      this.h5_chart_data = data.chart_data
    })
    chart.getUserMobileTransform(this.params).then((data) => {
      this.mobile_chart_data = data.chart_data
    })
  },
  methods: {
    drawH5Chart: function (data) {
      if (this.h5_chart) {
        this.h5_chart.source(data)
        this.h5_chart.repaint()
      } else {
        this.h5_chart = new G2.Chart({
          container: 'h5-transform',
          padding: [0, 100, 50, 100],
          height: 297,
          forceFit: true
        })
        this.h5_chart.source(data)
        this.h5_chart.axis(false)
        this.h5_chart.coord('react').transpose().scale(1, -1)
        this.h5_chart.intervalSymmetric().position('action*value').shape('pyramid').color('action', ['#0050B3', '#1890FF', '#40A9FF', '#69C0FF', '#BAE7FF']).label('action*value', function (action, value) {
          return action + ' ' + value
        }, {
          offset: 35,
          labelLine: {
            lineWidth: 1,
            stroke: 'rgba(0, 0, 0, 0.15)'
          }
        })
        this.h5_chart.tooltip({
          inPlot: true,
          follow: true,
          showTitle: false,
          itemTpl: '<li>{title}: {value}</li>'
        })
        this.h5_chart.render()
      }
    },
    drawMobileChart: function (data) {
      if (this.mobile_chart) {
        this.mobile_chart.source(data)
        this.mobile_chart.repaint()
      } else {
        this.mobile_chart = new G2.Chart({
          container: 'mobile-transform',
          padding: [0, 100, 50, 100],
          height: 297,
          forceFit: true
        })
        this.mobile_chart.source(data)
        this.mobile_chart.axis(false)
        this.mobile_chart.coord('react').transpose().scale(1, -1)
        this.mobile_chart.intervalSymmetric().position('action*value').shape('pyramid').color('action', ['#0050B3', '#1890FF', '#40A9FF', '#69C0FF', '#BAE7FF']).label('action*value', function (action, value) {
          return action + ' ' + value
        }, {
          offset: 35,
          labelLine: {
            lineWidth: 1,
            stroke: 'rgba(0, 0, 0, 0.15)'
          }
        })
        this.mobile_chart.tooltip({
          inPlot: true,
          follow: true,
          showTitle: false,
          itemTpl: '<li>{title}: {value}</li>'
        })
        this.mobile_chart.render()
      }
    },
    handleDatePickChange (val) {
      if (val) {
        this.params['sdate'] = format(this.dateRange[0], 'YYYY-MM-DD')
        this.params['edate'] = format(this.dateRange[1], 'YYYY-MM-DD')
      } else {
        delete this.params.sdate
        delete this.params.edate
      }
      chart.getUserH5Transform(this.params).then((data) => {
        this.h5_chart_data = data.chart_data
      })
      chart.getUserMobileTransform(this.params).then((data) => {
        this.mobile_chart_data = data.chart_data
      })
    }
  },
  watch: {
    h5_chart_data: function (val) {
      this.drawH5Chart(val)
    },
    mobile_chart_data: function (val) {
      this.drawMobileChart(val)
    }
  }
}
</script>
