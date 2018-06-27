<template>
  <div>
    <el-dialog
      title="方案信息"
      :visible.sync="visible">
      <el-form :model="form" label-width="120px">
        <el-form-item class="wrap" label="彩种：">
          {{ form.lottery_alias | filterLotteryName }}
        </el-form-item>
        <el-form-item class="wrap" label="奖期：">
          {{ form.lottery_period }}
        </el-form-item>
        <el-form-item class="wrap" label="开奖号码：">
          {{ form.bonus_code || '未开奖' }}
        </el-form-item>
        <el-form-item class="wrap" label="投注金额：">
          {{ form.total_money | filterMoney }}
        </el-form-item>
        <el-form-item class="wrap" label="红包金额：">
          {{ form.coupon_money | filterMoney }}
        </el-form-item>
        <el-form-item class="wrap" label="中奖金额：" v-if="form.bonus_money > 0">
          {{ form.bonus_money | filterMoney }}
        </el-form-item>
      </el-form>
      <el-table
        :data="form.tickets"
        border
        style="width: 100%">
        <el-table-column
          header-align="center"
          type="index"
          width="80">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="play_type"
          label="玩法">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="ante_code"
          label="投注号码">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="amount"
          label="倍数">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="投注金额">
          <template slot-scope="scope">
            {{ scope.row.total_money | filterMoney }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="中奖金额">
          <template slot-scope="scope">
            {{ scope.row.bonus_money | filterMoney }}
          </template>
        </el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
        <el-button @click="visible = false">关 闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import order from '../../api/order'

export default {
  data () {
    return {
      visible: false,
      form: {
        'lottery_alias': '',
        'lottery_period': '',
        'bonus_code': '',
        'total_money': '',
        'coupon_money': '',
        'bonus_money': '',
        'tickets': []
      }
    }
  },
  methods: {
    show (id) {
      order.retrieveNumberDetail(id).then((data) => {
        this.visible = true
        this.form = data
      })
    }
  },
  filters: {
    filterLotteryName (val) {
      let getLotteryName = {
        'qxc': '七星彩',
        'pl5': '排列5',
        'pl3': '出票成功/等待开奖',
        'dlc': '11选5(多乐彩)',
        'JXK3': '新快3',
        '3d': '福彩3D',
        'dlt': '大乐透',
        'ssq': '双色球'
      }
      return getLotteryName[val]
    },
    filterMoney (val) {
      return '￥' + val / 100
    }
  }
}
</script>

<style>
.wrap {
  text-align: left;
  word-wrap: break-word;
}
</style>
