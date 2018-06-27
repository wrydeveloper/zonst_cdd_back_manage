<template>
  <div>
    <el-date-picker
      size="small"
      v-model="dateRange"
      type="daterange"
      unlink-panels
      @change="handleDatePickChange"
      range-separator="至"
      start-placeholder="开始日期"
      end-placeholder="结束日期"
      :picker-options="pickerOptions">
    </el-date-picker>
  </div>
</template>
<script>
import { format } from 'date-fns'
export default {
  data () {
    return {
      dateRange: '',
      start_time: '',
      stop_time: '',
      pickerOptions: {
        shortcuts: [{
          text: '最近一周',
          onClick (picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近一个月',
          onClick (picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近三个月',
          onClick (picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
            picker.$emit('pick', [start, end])
          }
        }]
      }
    }
  },
  props: {
    type: {
      type: String,
      default: 'datetime'
    }
  },
  methods: {
    handleDatePickChange (val) {
      if (val) {
        if (this.type === 'date') {
          this.start_time = format(this.dateRange[0], 'YYYY-MM-DD')
          this.stop_time = format(this.dateRange[1], 'YYYY-MM-DD')
        } else {
          this.start_time = format(this.dateRange[0], 'YYYY-MM-DD 00:00:00')
          this.stop_time = format(this.dateRange[1], 'YYYY-MM-DD 23:59:59')
        }
      } else {
        this.start_time = ''
        this.stop_time = ''
      }
      this.$emit('change', this.start_time, this.stop_time)
    }
  }
}
</script>
