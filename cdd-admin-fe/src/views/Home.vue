<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="6">
        <v-chart-user></v-chart-user>
      </el-col>
      <el-col :span="9">
        <v-chart-sports></v-chart-sports>
      </el-col>
      <el-col :span="9">
        <v-chart-number></v-chart-number>
      </el-col>
    </el-row>
    <br>
    <el-row>
      <el-card>
        <el-col :span="15">
          <v-chart-sales-trend></v-chart-sales-trend>
        </el-col>
        <el-col :span="9">
          <v-chart-sales-rank></v-chart-sales-rank>
        </el-col>
      </el-card>
    </el-row>
    <br>
    <el-row :gutter="20">
      <el-col :span="12">
        <v-chart-transform></v-chart-transform>
      </el-col>
      <el-col :span="12">
        <v-chart-sales-scale></v-chart-sales-scale>
      </el-col>
    </el-row>
    <br>
    <el-row>
      <el-card>
        <h4>用户访问率</h4>
        <v-line></v-line>
      </el-card>
    </el-row>
  </div>
</template>

<script>
import VChartSports from '../components/charts/VChartSports'
import VChartNumber from '../components/charts/VChartNumber'
import VChartSalesTrend from '../components/charts/VChartSalesTrend'
import VChartSalesScale from '../components/charts/VChartSalesScale'
import VChartSalesRank from '../components/charts/VChartSalesRank'
import VChartTransform from '../components/charts/VChartTransform'
import VChartUser from '../components/charts/VChartUser'
import VLine from '../components/charts/VLine'

export default {
  components: {
    VChartSports,
    VChartNumber,
    VChartSalesTrend,
    VChartSalesScale,
    VChartSalesRank,
    VChartTransform,
    VChartUser,
    VLine
  }
}
</script>
