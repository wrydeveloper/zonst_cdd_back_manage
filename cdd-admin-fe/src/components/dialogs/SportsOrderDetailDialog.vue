<template>
  <div>
    <el-dialog
      title="方案信息"
      :visible.sync="visible">
      <el-form :model="form" label-width="120px">
        <el-form-item class="wrap" label="订单金额：">
          {{ form.bet_money | filterMoney }}
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
          label="场次">
          <template slot-scope="scope">
            {{ scope.row.match_number | filterMatchNumber }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="play_type"
          label="玩法">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="对阵">
          <template slot-scope="scope">
            {{ scope.row | filterTeam }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="投注项">
          <template slot-scope="scope">
            {{ [scope.row.match_number, scope.row.lottery_id, bets] | filterBet }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="彩果">
          <template slot-scope="scope">
            {{ scope.row | filterResult }}
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

import { dictPlayType } from '../../utils/dict'

export default {
  data () {
    return {
      visible: false,
      form: {
        'bet_money': '',
        'coupon_money': '',
        'bonus_money': '',
        'bet_codes': '',
        'tickets': []
      },
      bets: {}
    }
  },
  methods: {
    show (id) {
      order.retrieveSportsDetail(id).then((data) => {
        this.visible = true
        this.form = data
        this.convertBet(this.form.bet_codes)
      })
    },
    convertBet (bet) {
      let listBet = bet.split('^')
      for (var i in listBet) {
        let listItem = listBet[i].split('*')
        let key = listItem[0] + '*' + listItem[1] + '*' + listItem[2]
        this.bets[key] = listItem[3]
      }
    }
  },
  filters: {
    filterMatchNumber (val) {
      let listMatchNumber = val.split('*')
      let dictWeek = {
        '1': '周一',
        '2': '周二',
        '3': '周三',
        '4': '周四',
        '5': '周五',
        '6': '周六',
        '7': '周日'
      }
      return dictWeek[listMatchNumber[1]] + listMatchNumber[2]
    },
    filterTeam (val) {
      return val.home_team + ' vs ' + val.away_team
    },
    filterBet ([match, type, bets]) {
      let listValue = bets[match].split(',')
      var betList = []
      for (var i in listValue) {
        let betText = dictPlayType[type][listValue[i]]
        betList.push(betText)
      }
      return betList.join(',')
    },
    filterResult (val) {
      let getResult = {
        'FT01': val.ft01_result,
        'FT02': val.ft02_result,
        'FT03': val.ft03_result,
        'FT04': val.ft04_result,
        'FT05': val.ft05_result,
        'BT01': val.bt01_result,
        'BT02': val.bt02_result,
        'BT03': val.bt03_result,
        'BT04': val.bt04_result
      }
      return getResult[val.lottery_id] || '未开奖'
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
