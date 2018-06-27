<template>
  <div class="filter-item">
    <el-select v-model="option" placeholder="彩种" size="small" clearable @change="change">
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
          label: '七星彩',
          value: 'qxc'
        },
        {
          label: '排列5',
          value: 'pl5'
        },
        {
          label: '排列3',
          value: 'pl3'
        },
        {
          label: '11选5(多乐彩)',
          value: 'dlc'
        },
        {
          label: '新快3',
          value: 'JXK3'
        },
        {
          label: '福彩3D',
          value: '3d'
        },
        {
          label: '大乐透',
          value: 'dlt'
        },
        {
          label: '双色球',
          value: 'ssq'
        }
      ]
    }
  },
  created () {
    this.init(this.$route)
  },
  methods: {
    init (route) {
      if (route.query.lottery_alias) {
        this.option = route.query.lottery_alias
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
