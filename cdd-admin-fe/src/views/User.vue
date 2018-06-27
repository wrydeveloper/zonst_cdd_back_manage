<template>
  <div v-loading="loading">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card>汇总 <span class="statistic-span">{{ statistic.total_count }}</span> 个</el-card>
      </el-col>
      <el-col :span="6">
        <el-card>H5 <span class="statistic-span">{{ statistic.h5_count }}</span> 个</el-card>
      </el-col>
      <el-col :span="6">
        <el-card>Android <span class="statistic-span">{{ statistic.android_count }}</span> 个</el-card>
      </el-col>
      <el-col :span="6">
        <el-card>iOS <span class="statistic-span">{{ statistic.ios_count }}</span> 个</el-card>
      </el-col>
    </el-row>
    <br>
    <el-card>
      <el-row class="filter">
        <el-input style="width: 400px"
          @change="changeKeyword"
          size="small"
          placeholder="支持用户ID、手机号、姓名、昵称及银行账号查询"
          v-model="keyword"
          clearable>
        </el-input>
        <date-select style="display: inline-block;" @change="changeDate"></date-select>
        <channel-select @change="changeChannel"></channel-select>
        <platform-select @change="changePlatform"></platform-select>
        <el-button class="search-btn" type="primary" size="small" @click="handleSearch">查询</el-button>
      </el-row>
      <br />
      <el-table
        :data="users"
        style="width: 100%">
        <el-table-column
          header-align="center"
          type="index"
          width="80">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="用户ID">
          <template slot-scope="scope">
            <a v-if="user.role !== 'channel'" @click="retrieve(scope.row.id)">
              {{ scope.row.id }}
            </a>
            <div v-else>
              {{ scope.row.id }}
            </div>
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="phone_number"
          label="手机">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="channel"
          label="渠道">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="平台">
          <template slot-scope="scope">
            {{ scope.row.platform | filterPlatform }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="余额">
          <template slot-scope="scope">
            {{ scope.row.balance | filterMoney }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="invite_count"
          label="邀请人数">
          <template slot-scope="scope">
            <a v-if="scope.row.invite_count > 0" @click="listInvitee(scope.row.id)">
              {{ scope.row.invite_count }}
            </a>
            <div v-else>
              {{ scope.row.invite_count }}
            </div>
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="状态">
          <template slot-scope="scope">
            <el-tag
              size="mini"
              :type="handleStatusTagType(scope.row.status)">{{ scope.row.status | filterUserStatus }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="reg_time"
          label="注册时间"
          width="180">
        </el-table-column>
        <el-table-column
          label="操作"
          width="180"
          align="center">
          <template slot-scope="scope">
            <el-button size="mini" @click="handleUpdate(scope.row.id)">修改</el-button>
          </template>
        </el-table-column>
      </el-table>
      <br>
      <el-row type="flex" justify="center">
        <el-pagination
          background
          layout="prev, pager, next"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-size="pageSize"
          :total="total">
        </el-pagination>
      </el-row>
      <user-detail-dialog ref="userDetailDialog"></user-detail-dialog>
      <user-invitee-dialog ref="userInviteeDialog"></user-invitee-dialog>
      <user-channel-dialog ref="userChannelDialog" @confirm="handleConfirmUpdateChannel"></user-channel-dialog>
    </el-card>
  </div>
</template>

<script>
import user from '../localStorage/user'
import customer from '../api/user'

import UserDetailDialog from '../components/dialogs/UserDetailDialog'
import UserInviteeDialog from '../components/dialogs/UserInviteeDialog'
import UserChannelDialog from '../components/dialogs/UserChannelDialog'
import ChannelSelect from '../components/selects/ChannelSelect'
import PlatformSelect from '../components/selects/PlatformSelect'
import DateSelect from '../components/selects/DateSelect'

import { filterPlatform, filterUserStatus, filterMoney } from '../filters'

export default {
  data () {
    return {
      loading: false,
      user: {},
      users: [],
      statistic: {
        total_count: 0,
        h5_count: 0,
        android_count: 0,
        ios_count: 0
      },
      total: 0,
      currentPage: 1,
      pageSize: 10,
      params: {},
      keyword: '',
      channel: '',
      platform: '',
      dateRange: ''
    }
  },
  created () {
    this.init(this.$route)
    this.list(this.params)
    this.user = user
  },
  components: {
    UserDetailDialog,
    UserInviteeDialog,
    UserChannelDialog,
    ChannelSelect,
    PlatformSelect,
    DateSelect
  },
  methods: {
    changeDate (start, end) {
      if (start && end) {
        this.params['start_time'] = start
        this.params['stop_time'] = end
      } else {
        delete this.params.start_time
        delete this.params.stop_time
      }
    },
    init (route) {
      let startTime = null
      let stopTime = null
      if (route.query.pageSize) {
        this.params['page_size'] = route.query.pageSize
      }
      if (route.query.page) {
        this.params['page'] = route.query.page
        this.currentPage = parseInt(route.query.page)
      }
      if (route.query.keyword) {
        this.params['keyword'] = route.query.keyword
        this.keyword = route.query.keyword
      }
      if (route.query.start_time) {
        this.params['start_time'] = route.query.start_time
        startTime = new Date(route.query.start_time)
      }
      if (route.query.stop_time) {
        this.params['stop_time'] = route.query.stop_time
        stopTime = new Date(route.query.stop_time)
      }
      if (startTime && stopTime) {
        this.dateRange = [startTime, stopTime]
      }
      this.total = this.currentPage * 10
    },
    list (params) {
      this.loading = true
      customer.list(params).then((data) => {
        this.users = data.results.data
        this.total = data.count
        this.statistic = data.results.statistic
        this.loading = false
      })
    },
    retrieve (id) {
      this.$refs.userDetailDialog.show(id)
    },
    handleUpdate (id) {
      this.$refs.userChannelDialog.show(id)
    },
    handleConfirmUpdateChannel () {
      this.list(this.params)
    },
    listInvitee (id) {
      this.$refs.userInviteeDialog.show(id)
    },
    handleSearch () {
      this.currentPage = 1
      delete this.params.page
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'User', query: params })
    },
    changeKeyword (val) {
      if (val) {
        this.keyword = val
        this.params['keyword'] = val
      } else {
        this.keyword = ''
        delete this.params.keyword
      }
    },
    changeChannel (val) {
      if (val) {
        this.channel = val
        this.params['channel'] = val
      } else {
        this.channel = ''
        delete this.params.channel
      }
    },
    changePlatform (val) {
      if (val) {
        this.platform = val
        this.params['platform'] = val
      } else {
        this.platform = ''
        delete this.params.platform
      }
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.params['page'] = val
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'User', query: params })
    },
    handleStatusTagType (val) {
      if (val === 1) {
        return 'success'
      } else {
        return 'danger'
      }
    }
  },
  filters: {
    filterPlatform,
    filterUserStatus,
    filterMoney
  },
  watch: {
    $route: {
      deep: true,
      handler: function (val) {
        if (val.name === 'User') {
          this.init(val)
          this.list(this.params)
        }
      }
    }
  }
}
</script>
