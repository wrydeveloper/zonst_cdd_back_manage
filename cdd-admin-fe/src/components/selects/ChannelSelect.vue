<template>
  <div class="filter-item">
    <el-select
      v-model="option"
      placeholder="渠道"
      size="small"
      clearable
      filterable
      @change="change">
      <el-option
        v-for="item in options"
        :key="item.id"
        :label="item.id"
        :value="item.id">
      </el-option>
    </el-select>
  </div>
</template>

<script>
import channel from '../../api/channel'

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
      if (route.query.channel) {
        this.option = route.query.channel
        this.$emit('change', this.option)
      }
    },
    list () {
      channel.listOption().then((data) => {
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
