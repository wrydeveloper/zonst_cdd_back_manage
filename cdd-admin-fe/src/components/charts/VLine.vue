<template>
  <div id="c4"></div>
</template>

<script>
import G2 from '@antv/g2'
import { DataSet } from '@antv/data-set'

export default {
  data () {
    return {
      chart: null,
      data: [
        { date: '2018-05-31', h5: 50, android: 30, ios: 10 },
        { date: '2018-05-30', h5: 45, android: 25, ios: 5 },
        { date: '2018-05-29', h5: 40, android: 20, ios: 10 },
        { date: '2018-05-28', h5: 35, android: 15, ios: 5 },
        { date: '2018-05-27', h5: 30, android: 10, ios: 10 },
        { date: '2018-05-26', h5: 25, android: 5, ios: 5 },
        { date: '2018-05-25', h5: 20, android: 30, ios: 10 },
        { date: '2018-05-24', h5: 15, android: 25, ios: 5 },
        { date: '2018-05-23', h5: 10, android: 20, ios: 10 },
        { date: '2018-05-22', h5: 5, android: 15, ios: 5 },
        { date: '2018-05-21', h5: 50, android: 10, ios: 10 },
        { date: '2018-05-20', h5: 45, android: 5, ios: 5 },
        { date: '2018-05-19', h5: 40, android: 30, ios: 10 },
        { date: '2018-05-18', h5: 35, android: 25, ios: 5 },
        { date: '2018-05-17', h5: 30, android: 20, ios: 10 },
        { date: '2018-05-16', h5: 25, android: 15, ios: 5 },
        { date: '2018-05-15', h5: 20, android: 10, ios: 10 },
        { date: '2018-05-14', h5: 15, android: 5, ios: 5 },
        { date: '2018-05-13', h5: 10, android: 30, ios: 10 },
        { date: '2018-05-12', h5: 5, android: 25, ios: 5 },
        { date: '2018-05-11', h5: 50, android: 20, ios: 10 },
        { date: '2018-05-09', h5: 45, android: 15, ios: 5 },
        { date: '2018-05-08', h5: 40, android: 10, ios: 10 },
        { date: '2018-05-07', h5: 35, android: 5, ios: 5 },
        { date: '2018-05-06', h5: 30, android: 30, ios: 10 },
        { date: '2018-05-05', h5: 25, android: 25, ios: 5 },
        { date: '2018-05-04', h5: 20, android: 20, ios: 10 },
        { date: '2018-05-03', h5: 15, android: 15, ios: 5 },
        { date: '2018-05-02', h5: 10, android: 10, ios: 10 },
        { date: '2018-05-01', h5: 5, android: 5, ios: 5 }
      ]
    }
  },
  mounted () {
    this.drawChart(this.data)
  },
  methods: {
    drawChart: function (data) {
      let ds = new DataSet()
      let dv = ds.createView().source(data)
      dv.transform({
        type: 'fold',
        fields: ['h5', 'android', 'ios'],
        key: 'platform',
        value: 'count'
      })
      this.chart = new G2.Chart({
        container: 'c4',
        forceFit: true,
        padding: [100, 100, 100, 100],
        width: 1100,
        height: 360
      })
      this.chart.source(dv)
      this.chart.tooltip({
        crosshairs: {
          type: 'line'
        }
      })
      this.chart.line().position('date*count').color('platform')
      this.chart.point().position('date*count').color('platform').shape('circle').style({
        stroke: '#fff',
        lineWidth: 1
      })
      this.chart.render()
    }
  }
}
</script>
