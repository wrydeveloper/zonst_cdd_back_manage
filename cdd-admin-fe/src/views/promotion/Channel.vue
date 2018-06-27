<template>
  <div v-loading="loading">
    <el-card>
      <el-row class="filter">
        <el-input style="width: 400px;"
          size="small"
          placeholder="请选输入渠道号"
          v-model="keyword"
          @change="changeKeyword"
          @keyup.enter.native="handleSearch"
          clearable>
        </el-input>
        <proxy-select v-if="user.role === 'commerce'" @change="changeProxy"></proxy-select>
        <el-button class="search-btn" type="primary" size="small" @click="handleSearch">查询</el-button>
        <el-button class="add-btn" size="small" @click="handleAdd"><i class="el-icon-plus"></i> 添加渠道</el-button>
      </el-row>
      <br />
      <el-table
        :data="channels"
        style="width: 100%">
        <el-table-column
          header-align="center"
          type="index"
          width="80">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="渠道号"
          width="100">
          <template slot-scope="scope">
            <el-button
              @click.native.prevent="retrieve(scope.row.id)"
              type="text"
              size="medium">
              {{ scope.row.id }}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column v-if="user.role === 'commerce'"
          header-align="center"
          label="所属代理"
          width="100">
          <template slot-scope="scope">
            <el-button
              @click.native.prevent="getProxyDetail(scope.row.proxy_id)"
              type="text"
              size="medium">
              {{ scope.row.proxy_name }}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="commission"
          label="CPS比例"
          width="80">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="promotion_url"
          label="推广链接">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="h5_url"
          label="H5链接">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="android_url"
          label="android链接">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="ios_url"
          label="iOS链接">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="是否占用"
          width="80">
          <template slot-scope="scope">
            {{ scope.row.is_used | filterIsUsed }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="状态"
          width="80">
          <template slot-scope="scope">
            <el-tag
              size="mini"
              :type="handleStatusTagType(scope.row.status)">{{ scope.row.status | filterPromotionStatus }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="mark"
          label="备注">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="add_time"
          label="创建时间"
          width="180">
        </el-table-column>
        <el-table-column
          label="操作"
          width="180"
          align="center">
          <template slot-scope="scope">
            <el-button size="mini" @click="handleEdit(scope.row.id)">编辑</el-button>
            <!-- <el-button type="danger" size="mini" @click="handleDelete(scope.row.id)">删除</el-button> -->
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
      <proxy-detail-dialog ref="proxyDetailDialog"></proxy-detail-dialog>
      <channel-detail-dialog ref="channelDetailDialog"></channel-detail-dialog>
      <el-dialog
        width="30%"
        :visible.sync="channelFormVisable"
        :show-close="false"
        :close-on-press-escape="false"
        :close-on-click-modal="false">
        <div slot="title">
          {{ formTitle }}
        </div>
        <el-form :model="channelForm" :rules="channelRule" ref="channelForm" label-width="120px">
          <el-form-item label="姓名" prop="real_name">
            <el-input v-model="channelForm.real_name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="手机号码" prop="phone">
            <el-input v-model="channelForm.phone" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="所属代理" prop="proxy_id" v-if="user.role === 'commerce'">
            <el-select v-model="channelForm.proxy_id" style="width: 100%;" placeholder="请选择">
              <el-option
                v-for="item in proxy_option_list"
                :key="item.id"
                :label="item.proxy_name"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="CPS比例" prop="commission">
            <el-input v-model="channelForm.commission" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="备注" prop="mark">
            <el-input v-model="channelForm.mark" auto-complete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="resetForm('channelForm')">取 消</el-button>
          <el-button type="primary" @click="submitForm('channelForm')">确 定</el-button>
        </div>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
import channel from '../../api/channel'
import proxy from '../../api/proxy'
import user from '../../localStorage/user'

import ProxyDetailDialog from '../../components/dialogs/ProxyDetailDialog'
import ChannelDetailDialog from '../../components/dialogs/ChannelDetailDialog'
import ProxySelect from '../../components/selects/ProxySelect'

import { filterPromotionStatus } from '../../filters'

export default {
  data () {
    return {
      loading: false,
      channels: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      params: {},
      keyword: '',
      proxy_id: '',
      channelFormVisable: false,
      channelForm: {
        proxy_id: '',
        commission: 0,
        is_used: '',
        mark: ''
      },
      channelRule: {},
      formTitle: '添加渠道',
      formAction: 'create',
      proxy_option_list: []
    }
  },
  created () {
    this.user = user
    this.init(this.$route)
    this.list(this.params)
    if (this.user.role === 'commerce') {
      this.listProxyOption()
    }
  },
  components: {
    ProxyDetailDialog,
    ChannelDetailDialog,
    ProxySelect
  },
  methods: {
    init (route) {
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
      if (route.query.proxy_id) {
        this.params['proxy_id'] = route.query.proxy_id
        this.proxy_id = parseInt(route.query.proxy_id)
      }
      this.total = this.currentPage * 10
    },
    list (params) {
      this.loading = true
      channel.list(params).then((data) => {
        this.channels = data.results
        this.total = data.count
        this.loading = false
      })
    },
    retrieve (id) {
      this.$refs.channelDetailDialog.show(id)
    },
    listProxyOption () {
      proxy.listOption().then((data) => {
        this.proxy_option_list = data
      })
    },
    getProxyDetail (id) {
      this.$refs.proxyDetailDialog.show(id)
    },
    handleAdd () {
      this.channelForm = {}
      this.formTitle = '添加渠道'
      this.formAction = 'create'
      this.channelFormVisable = true
    },
    handleEdit (id) {
      this.formTitle = '编辑渠道'
      this.formAction = 'update'
      channel.retrieve(id).then((data) => {
        this.channelFormVisable = true
        this.channelForm = data
      })
    },
    handleDelete (id) {
      this.$confirm('此操作将永久删除该渠道, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        channel.destory(id).then((data) => {
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
          this.list(this.params)
        }).catch((error) => {
          this.$message({
            type: 'warning',
            message: error.message
          })
        })
      })
    },
    submitForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let data = this.channelForm
          if (this.formAction === 'create') {
            channel.create(data).then((data) => {
              this.channelFormVisable = false
              this.$message({
                type: 'success',
                message: '添加成功!'
              })
              this.list()
            }).catch((error) => {
              this.$message({
                type: 'warning',
                message: error.message
              })
            })
          } else {
            let id = this.channelForm.id
            channel.update(id, data).then((data) => {
              this.channelFormVisable = false
              this.$message({
                type: 'success',
                message: '编辑成功!'
              })
              this.list(this.params)
            }).catch((error) => {
              this.$message({
                type: 'warning',
                message: error.message
              })
            })
          }
        }
      })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
      this.channelFormVisable = false
    },
    handleSearch () {
      this.currentPage = 1
      delete this.params.page
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'PromotionChannel', query: params })
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
    changeProxy (val) {
      if (val) {
        this.proxy_id = val
        this.params['proxy_id'] = val
      } else {
        this.proxy_id = ''
        delete this.params.proxy_id
      }
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.params['page'] = val
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'PromotionChannel', query: params })
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
    filterPromotionStatus,
    filterIsUsed (val) {
      let getIsUsed = {
        0: '占用',
        1: '可用'
      }
      return getIsUsed[val]
    }
  },
  watch: {
    $route: {
      deep: true,
      handler: function (val) {
        if (val.name === 'PromotionChannel') {
          this.init(val)
          this.list(this.params)
        }
      }
    }
  }
}
</script>
