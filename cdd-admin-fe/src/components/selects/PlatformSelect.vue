<template>
  <div class="filter-item">
    <el-select v-model="option" placeholder="平台" size="small" clearable @change="change">
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
          label: 'H5',
          value: '1'
        },
        {
          label: 'Android',
          value: '2'
        },
        {
          label: 'iOS',
          value: '3'
        }
      ]
    }
  },
  created () {
    this.init(this.$route)
  },
  methods: {
    init (route) {
      if (route.query.platform) {
        this.option = route.query.platform
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
