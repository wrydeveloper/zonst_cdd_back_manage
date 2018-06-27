<template>
  <div class="filter-item">
    <el-select
      v-model="option"
      placeholder="代理"
      size="small"
      clearable
      filterable
      @change="change">
      <el-option
        v-for="item in options"
        :key="item.id"
        :label="item.proxy_name"
        :value="item.id">
      </el-option>
    </el-select>
  </div>
</template>

<script>
import proxy from '../../api/proxy'

export default {
  data () {
    return {
      option: '',
      options: []
    }
  },
  created () {
    this.init(this.$route)
    this.list()
  },
  methods: {
    init (route) {
      if (route.query.proxy) {
        this.option = route.query.proxy
        this.$emit('change', this.option)
      }
    },
    list () {
      proxy.listOption().then((data) => {
        this.options = data
      })
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
