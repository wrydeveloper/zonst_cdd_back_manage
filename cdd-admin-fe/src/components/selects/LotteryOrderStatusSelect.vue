<template>
  <div class="filter-item">
    <el-select v-model="option" placeholder="状态" size="small" clearable @change="change">
      <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value">
      </el-option>
    </el-select>
  </div>
</template>

<script>
export default {
  data () {
    return {
      option: '',
      options: [
        {
          label: '待支付',
          value: '0'
        },
        {
          label: '支付成功/等待出票',
          value: '1'
        },
        {
          label: '出票成功/等待开奖',
          value: '2'
        },
        {
          label: '出票失败/等待退款',
          value: '3'
        },
        {
          label: '已退款',
          value: '4'
        },
        {
          label: '未中奖',
          value: '5'
        },
        {
          label: '已中奖',
          value: '6'
        },
        {
          label: '部分出票成功/待开奖',
          value: '7'
        }
      ]
    }
  },
  created () {
    this.init(this.$route)
  },
  methods: {
    init (route) {
      if (route.query.order_status) {
        this.option = route.query.order_status
        this.$emit('change', this.option)
      }
    },
    change () {
      this.$emit('change', this.option)
    }
  }
}
</script>

<style>
.filter-item {
  display: inline-block;
  position: relative;
}
</style>
