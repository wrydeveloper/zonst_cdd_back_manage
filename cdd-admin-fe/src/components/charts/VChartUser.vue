<template>
  <el-card class="card">
    <div class="card-header">
      <div class="meta">
        <div class="analysis-label">今日用户总数</div>
        <div class="analysis-total">{{ user.total_count }}</div>
      </div>
    </div>
    <div class="card-content">
      <div class="fixed">
        H5 <span>{{ user.h5_count }}</span>
        Android <span>{{ user.android_count }}</span>
        iOS <span>{{ user.ios_count }}</span>
      </div>
    </div>
    <div class="card-footer">
      昨日留存 <span>{{ user.rate }}%</span>
    </div>
  </el-card>
</template>

<script>
import chart from '../../api/chart'

export default {
  data () {
    return {
      user: {}
    }
  },
  created () {
    chart.getUser().then((data) => {
      this.user = data
    })
  }
}
</script>
