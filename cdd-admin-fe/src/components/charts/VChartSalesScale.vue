<template>
  <el-card>
    <h4>销售额彩种占比
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
    <div id="sales-scale" style="width: 500px;"></div>
  </el-card>
</template>

<script>
import { format } from 'date-fns'
import chart from '../../api/chart'

import G2 from '@antv/g2'
import { DataSet } from '@antv/data-set'

export default {
  data () {
    return {
      chart: null,
      dv: null,
      chart_data: [],
      total_money: '',
      params: {},
      dateRange: ''
    }
  },
  created () {
    chart.getSalesScale(this.params).then((data) => {
      this.chart_data = data.chart_data
      this.total_money = data.total_money
    })
  },
  methods: {
    drawChart: function (data) {
      if (this.chart) {
        this.dv.source(data)
        this.chart.source(this.dv)
        this.chart.repaint()
      } else {
        let _DataSet = DataSet
        let DataView = _DataSet.DataView
        this.dv = new DataView()
        this.dv.source(data).transform({
          type: 'percent',
          field: 'count',
          dimension: 'item',
          as: 'percent'
        })
        this.chart = new G2.Chart({
          container: 'sales-scale',
          padding: [30, 0, 0, 0],
          width: 500,
          height: 360,
          forceFit: true
        })
        this.chart.source(this.dv, {
          percent: {
            formatter: function formattter (val) {
              val = (val * 100).toFixed(2) + '%'
              return val
            }
          }
        })
        this.chart.legend({
          useHtml: true,
          position: 'right',
          containerTpl: '<div class="g2-legend">' +
            '<table class="g2-legend-list" style="list-style-type:none;margin:0;padding:0;text-align:left;"></table>' +
            '</div>',
          itemTpl: (value, color, checked, index) => {
            const obj = this.dv.rows[index]
            checked = checked ? 'checked' : 'unChecked'
            return '<tr class="g2-legend-list-item item-' + index + ' ' + checked +
              '" data-value="' + value + '" data-color=' + color +
              ' style="cursor: pointer;font-size: 14px;">' +
              '<td width=350 style="border: none;padding:0;"><i class="g2-legend-marker" style="width:10px;height:10px;display:inline-block;margin-right:10px;background-color:' + color + ';"></i>' +
              '<span class="g2-legend-text">' + value + '</span></td>' +
              '<td style="text-align: right;border: none;padding:0;">' + '￥' + obj.count / 100 + '</td>' +
              '</tr>'
          },
          offsetX: 15,
          'g2-legend': {
            width: '200px',
            marginLeft: '-40px',
            marginTop: '-70px'
          },
          'g2-legend-list': {
            border: 'none'
          }
        })
        this.chart.coord('theta', {
          radius: 0.75,
          innerRadius: 0.75
        })
        this.chart.tooltip({
          showTitle: false,
          itemTpl: '<li><span style="background-color:{color};" class="g2-tooltip-marker"></span>{name}: {value}</li>'
        })
        this.chart.guide().html({
          position: ['50%', '50%'],
          html: '<div style="color:#8c8c8c;font-size: 14px;text-align: center;width: 10em;">销售额<br><span style="color:#8c8c8c;font-size:20px">' + '￥' + this.total_money + '</span></div>',
          alignX: 'middle',
          alignY: 'middle'
        })
        this.chart.intervalStack().position('percent').color('item').tooltip('item*percent', function (item, percent) {
          percent = (percent * 100).toFixed(2) + '%'
          return {
            name: item,
            value: percent
          }
        }).style({
          lineWidth: 5,
          stroke: '#fff'
        })
        this.chart.render()
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
      chart.getSalesScale(this.params).then((data) => {
        this.chart_data = data.chart_data
        this.total_money = data.total_money
      })
    }
  },
  watch: {
    chart_data: function (val) {
      this.drawChart(val)
    }
  }
}
</script>
