
export const filterPlatform = (val) => {
  let dictPlatform = {
    1: 'H5',
    2: 'Android',
    3: 'iOS'
  }
  return dictPlatform[val]
}

export const filterUserStatus = (val) => {
  let dictUserStatus = {
    1: '已启用',
    2: '已禁用'
  }
  return dictUserStatus[val]
}

export const filterMoney = (val) => {
  return '￥' + val / 100
}

export const filterRate = (val) => {
  return val + '%'
}

export const filterPayType = (val) => {
  let dictPayType = {
    'wechat_pay': '微信',
    'ali_pay': '支付宝'
  }
  return dictPayType[val]
}

export const filterChannelStatus = (val) => {
  let dictChannelStatus = {
    0: '未启用',
    1: '正常',
    2: '已解决'
  }
  return dictChannelStatus[val]
}

export const filterLotteryStatus = (val) => {
  let dictLotteryStatus = {
    0: '已下线',
    1: '已上线',
    2: '已暂停'
  }
  return dictLotteryStatus[val]
}

export const filterLotteryType = (val) => {
  let dictLotteryType = {
    1: '普通彩',
    2: '高频彩',
    3: '竞技彩'
  }
  return dictLotteryType[val]
}

export const filterMerchantStatus = (val) => {
  let dictMerchantStatus = {
    0: '未启用',
    1: '正常',
    2: '已解决'
  }
  return dictMerchantStatus[val]
}

export const filterMerchantPayType = (val) => {
  let dictMetchantPayType = {
    1: '微信',
    2: '支付宝',
    3: '银行卡'
  }
  return dictMetchantPayType[val]
}

export const filterRechargeStatus = (val) => {
  let dictRechargeStatus = {
    0: '待支付',
    1: '已成功'
  }
  return dictRechargeStatus[val]
}

export const filterRechargePayType = (val) => {
  let dictRechargePayType = {
    0: '余额',
    1: '微信',
    2: '支付宝',
    3: '银行卡'
  }
  return dictRechargePayType[val]
}

export const filterWithdrawStatus = (val) => {
  let dictWithdrawStatus = {
    0: '待处理',
    1: '已成功',
    2: '已失败',
    3: '已审核'
  }
  return dictWithdrawStatus[val]
}

export const filterLotteryBonusStatus = (val) => {
  let dictLotteryBonusStatus = {
    0: '未返奖',
    1: '已返奖'
  }
  return dictLotteryBonusStatus[val]
}

export const filterNumberLotteryType = (val) => {
  let dictNumberLotteryType = {
    'qxc': '七星彩',
    'pl5': '排列5',
    'pl3': '出票成功/等待开奖',
    'dlc': '11选5(多乐彩)',
    'JXK3': '新快3',
    '3d': '福彩3D',
    'dlt': '大乐透',
    'ssq': '双色球'
  }
  return dictNumberLotteryType[val]
}

export const filterIsBigAward = (val) => {
  let dictIsBigAward = {
    0: '否',
    1: '是'
  }
  return dictIsBigAward[val]
}

export const filterSportsLotteryType = (val) => {
  let dictSportsLotteryType = {
    'FT': '足球',
    'BT': '篮球'
  }
  return dictSportsLotteryType[val]
}

export const filterNumberLotteryPeriodStatus = (val) => {
  let dictNumberLotteryPeriodStatus = {
    0: '未开启',
    1: '开启新奖期',
    2: '暂停销售'
  }
  return dictNumberLotteryPeriodStatus[val] || '完成开奖'
}

export const filterOrderStatus = (val) => {
  let dictOrderStatus = {
    0: '待支付',
    1: '支付成功/等待出票',
    2: '出票成功/等待开奖',
    3: '出票失败/等待退款',
    4: '已退款',
    5: '未中奖',
    6: '已中奖',
    7: '部分出票成功/待开奖'
  }
  return dictOrderStatus[val]
}

export const filterFollowStatus = (val) => {
  let dictFollowStatus = {
    0: '停止追号',
    1: '正常追号',
    2: '完成追号'
  }
  return dictFollowStatus[val]
}

export const filterPayStatus = (val) => {
  let dictPayStatus = {
    success: '已成功',
    failed: '已失败',
    refund: '已退款'
  }
  return dictPayStatus[val]
}

export const filterPromotionStatus = (val) => {
  let dictPromotionStatus = {
    0: '已禁用',
    1: '已启用',
    2: '已下线'
  }
  return dictPromotionStatus[val]
}

export const filterPromotionType = (val) => {
  let dictPromotionType = {
    1: 'CPS',
    2: 'CPA',
    3: 'CPD',
    4: 'cpc',
    5: 'CPM'
  }
  return dictPromotionType[val]
}

export const filterPromotionPayType = (val) => {
  let dictPromotionPayType = {
    1: '月结',
    2: '周结',
    3: '日结'
  }
  return dictPromotionPayType[val] || '未知'
}

export const filterPromotionLevel = (val) => {
  let dictPromotionLevel = {
    0: '普通',
    1: '代理商'
  }
  return dictPromotionLevel[val]
}

export const filterBetType = (val) => {
  var arr = val.split('')
  var str = ''
  for (var i = 1; i <= 8; i++) {
    if (arr[i] === '0') {
      break
    } else if (arr[i] === '1') {
      str = arr[0] + '场单关投注,'
    } else {
      str += arr[i] + '串1,'
    }
  }
  str = str.substring(0, str.length - 1)
  return str
}
