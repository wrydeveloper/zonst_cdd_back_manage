<template>
  <div v-loading="loading">
    <el-card>
      <el-row class="filter">
        <el-input style="width: 400px;"
          size="small"
          placeholder="请选输入代理名称"
          v-model="keyword"
          @change="changeKeyword"
          @keyup.enter.native="handleSearch"
          clearable>
        </el-input>
        <el-select v-model="bd_id" placeholder="商务" size="small" clearable @change="changeBd">
          <el-option
            v-for="item in bd_option_list"
            :key="item.id"
            :label="item.bd_name"
            :value="item.id">
          </el-option>
        </el-select>
        <el-button class="search-btn" type="primary" size="small" @click="handleSearch" >查询</el-button>
        <el-button class="add-btn" size="small" @click="handleAdd"><i class="el-icon-plus"></i> 添加代理</el-button>
      </el-row>
      <br />
      <el-table
        :data="proxies"
        style="width: 100%">
        <el-table-column
          header-align="center"
          type="index"
          width="80">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="proxy_name"
          label="名称">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="所属商务">
          <template slot-scope="scope">
            <el-button
              @click.native.prevent="getCommerceDetail(scope.row.bd_id)"
              type="text"
              size="medium">
              {{ scope.row.bd_name }}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="phone"
          label="电话">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="等级">
          <template slot-scope="scope">
            {{ scope.row.proxy_level | filterPromotionLevel }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="类型">
          <template slot-scope="scope">
            {{ scope.row.proxy_type | filterPromotionType }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="commission"
          label="比例/单价">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="结算周期">
          <template slot-scope="scope">
            {{ scope.row.pay_type | filterPromotionPayType }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="状态">
          <template slot-scope="scope">
            <el-tag
              size="mini"
              :type="handleStatusTagType(scope.row.status)">{{ scope.row.status | filterPromotionStatus }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="add_time"
          width="180px"
          label="创建时间">
        </el-table-column>
        <el-table-column
          label="操作"
          width="240px"
          align="center">
          <template slot-scope="scope">
            <el-button size="mini" @click="handleEdit(scope.row.id)">编辑</el-button>
            <!-- <el-button type="danger" size="mini" @click="handleDelete(scope.row.id)">删除</el-button> -->
            <el-button type="primary" size="mini" @click="goChannel(scope.row.id)">渠道列表</el-button>
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
      <el-dialog
        width="25%"
        :visible.sync="commerceFormVisable"
        :show-close="false"
        :close-on-press-escape="false"
        :close-on-click-modal="false">
        <div slot="title">
          商务信息
        </div>
        <el-form :model="commerceForm" label-width="120px">
          <el-form-item class="wrap" label="商务工号：">
            {{ commerceForm.bd_id }}
          </el-form-item>
          <el-form-item class="wrap" label="商务姓名：">
            {{ commerceForm.bd_name }}
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="commerceFormVisable = false">关 闭</el-button>
        </div>
      </el-dialog>
      <el-dialog
        width="30%"
        :visible.sync="proxyFormVisable"
        :show-close="false"
        :close-on-press-escape="false"
        :close-on-click-modal="false">
        <div slot="title">
          {{ formTitle }}
        </div>
        <el-form :model="proxyForm" :rules="proxyRule" ref="proxyForm" label-width="120px">
          <el-form-item label="代理名称" prop="proxy_name">
            <el-input v-model="proxyForm.proxy_name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="公司名称" prop="company_name">
            <el-input v-model="proxyForm.company_name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="真实姓名" prop="real_name">
            <el-input v-model="proxyForm.real_name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="联系电话" prop="phone">
            <el-input v-model="proxyForm.phone" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="QQ" prop="qq">
            <el-input v-model="proxyForm.qq" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="所属商务" prop="bd_id">
            <el-select v-model="proxyForm.bd_id" style="width: 100%;" placeholder="请选择">
              <el-option
                v-for="item in bd_option_list"
                :key="item.id"
                :label="item.bd_name"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="代理等级" prop="proxy_level">
            <el-select v-model="proxyForm.proxy_level" style="width: 100%;" placeholder="请选择代理等级">
              <el-option label="普通" :value="0"></el-option>
              <el-option label="代理商" :value="1"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="代理类型" prop="proxy_type">
            <el-select v-model="proxyForm.proxy_type" style="width: 100%;" placeholder="请选择代理类型">
              <el-option label="CPS" :value="1"></el-option>
              <el-option label="CPA" :value="2"></el-option>
              <el-option label="CPD" :value="3"></el-option>
              <el-option label="CPC" :value="4"></el-option>
              <el-option label="CPM" :value="5"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="比例/单价" prop="commission">
            <el-input-number v-model="proxyForm.commission" style="width: 100%;" placeholder="请输入比例/单价" controls-position="right"></el-input-number>
          </el-form-item>
          <el-form-item label="结算周期" prop="pay_type">
            <el-select v-model="proxyForm.pay_type" style="width: 100%;" placeholder="请选择结算周期">
              <el-option label="月结" :value="1"></el-option>
              <el-option label="周结" :value="2"></el-option>
              <el-option label="日结" :value="3"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="银行卡号" prop="bank_number">
            <el-input v-model="proxyForm.bank_number" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="开户姓名" prop="bank_account">
            <el-input v-model="proxyForm.bank_account" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="开户行" prop="bank_name">
            <el-input v-model="proxyForm.bank_name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="支行地址" prop="bank_addr">
            <el-input v-model="proxyForm.bank_addr" auto-complete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="resetForm('proxyForm')">取 消</el-button>
          <el-button type="primary" @click="submitForm('proxyForm')">确 定</el-button>
        </div>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
import proxy from '../../api/proxy'
import commerce from '../../api/commerce'

import { filterPromotionStatus, filterPromotionType, filterPromotionPayType, filterPromotionLevel } from '../../filters'

export default {
  data () {
    return {
      loading: false,
      proxies: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      params: {},
      keyword: '',
      bd_id: '',
      proxyFormVisable: false,
      proxyForm: {
        proxy_name: '',
        company_name: '',
        phone: '',
        qq: '',
        bd_id: '',
        proxy_level: '',
        proxy_type: '',
        commission: 0,
        pay_type: '',
        real_name: '',
        bank_account: '',
        bank_name: '',
        bank_number: '',
        bank_addr: '',
        status: ''
      },
      proxyRule: {
        proxy_name: [
          { required: true, message: '请输入代理名称', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入手机号码', trigger: 'blur' }
        ],
        bd_id: [
          { required: true, message: '请选择所属商务', trigger: 'blur' }
        ],
        proxy_level: [
          { required: true, message: '请选择代理等级', trigger: 'blur' }
        ],
        proxy_type: [
          { required: true, message: '请选择代理类型', trigger: 'blur' }
        ],
        commission: [
          { required: true, message: '请输入比例或单价', trigger: 'blur' }
        ],
        pay_type: [
          { required: true, message: '请选择结算方式', trigger: 'blur' }
        ],
        real_name: [
          { required: true, message: '请输入真实姓名', trigger: 'blur' }
        ],
        bank_account: [
          { required: true, message: '请输入账户姓名', trigger: 'blur' }
        ],
        bank_name: [
          { required: true, message: '请输入开户行', trigger: 'blur' }
        ],
        bank_number: [
          { required: true, message: '请输入银行卡号', trigger: 'blur' }
        ],
        bank_addr: [
          { required: true, message: '请输入支行地址', trigger: 'blur' }
        ]
      },
      formTitle: '添加代理',
      formAction: 'create',
      bd_option_list: [],
      commerceForm: {},
      commerceFormVisable: false
    }
  },
  created () {
    this.init(this.$route)
    this.list(this.params)
    this.listCommerceOption()
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
      if (route.query.bd_id) {
        this.params['bd_id'] = route.query.bd_id
        this.bd_id = parseInt(route.query.bd_id)
      }
      this.total = this.currentPage * 10
    },
    list (params) {
      this.loading = true
      proxy.list(params).then((data) => {
        this.proxies = data.results
        this.total = data.count
        this.loading = false
      })
    },
    listCommerceOption () {
      commerce.listOption().then((data) => {
        this.bd_option_list = data
      })
    },
    getCommerceDetail (id) {
      commerce.retrieve(id).then((data) => {
        this.commerceFormVisable = true
        this.commerceForm = data
      })
    },
    goChannel (proxyID) {
      let query = {
        proxy_id: proxyID
      }
      this.$router.push({ name: 'PromotionChannel', query: query })
    },
    handleAdd () {
      this.proxyForm = {}
      this.formTitle = '添加代理'
      this.formAction = 'create'
      this.proxyFormVisable = true
    },
    handleEdit (id) {
      this.formTitle = '编辑代理'
      this.formAction = 'update'
      proxy.retrieve(id).then((data) => {
        this.proxyFormVisable = true
        this.proxyForm = data
      })
    },
    handleDelete (id) {
      this.$confirm('此操作将永久删除该代理, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        proxy.destory(id).then((data) => {
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
          let data = this.proxyForm
          if (this.formAction === 'create') {
            proxy.create(data).then((data) => {
              this.proxyFormVisable = false
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
            let id = this.proxyForm.id
            proxy.update(id, data).then((data) => {
              this.proxyFormVisable = false
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
      this.proxyFormVisable = false
    },
    handleSearch () {
      this.currentPage = 1
      delete this.params.page
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'PromotionProxy', query: params })
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
    changeBd (val) {
      if (val) {
        this.bd_id = val
        this.params['bd_id'] = val
      } else {
        this.bd_id = ''
        delete this.params.bd_id
      }
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.params['page'] = val
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'PromotionProxy', query: params })
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
    filterPromotionLevel,
    filterPromotionType,
    filterPromotionPayType
  },
  watch: {
    $route: {
      deep: true,
      handler: function (val) {
        if (val.name === 'PromotionProxy') {
          this.init(val)
          this.list(this.params)
        }
      }
    }
  }
}
</script>
