<template>
  <div v-loading="loading">
    <el-card>
      <el-row class="add-btn">
        <el-button size="small" @click="handleAdd"><i class="el-icon-plus"></i> 添加支付商</el-button>
      </el-row>
      <br />
      <el-table
        :data="merchants"
        style="width: 100%">
        <el-table-column
          header-align="center"
          type="index"
          width="80">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="company_name"
          label="公司名称">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="支付类型">
          <template slot-scope="scope">
            {{ scope.row.pay_type | filterMerchantPayType }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="rate"
          label="费率">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="appid"
          label="appid">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="appkey"
          label="appkey">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="状态">
          <template slot-scope="scope">
            {{ scope.row.status | filterMerchantStatus }}
          </template>
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
      <el-dialog
        width="30%"
        :visible.sync="merchantFormVisable"
        :show-close="false"
        :close-on-press-escape="false"
        :close-on-click-modal="false">
        <div slot="title">
          {{ formTitle }}
        </div>
        <el-form :model="merchantForm" :rules="merchantRule" ref="merchantForm" label-width="120px">
          <el-form-item label="公司名称" prop="company_name">
            <el-input v-model="merchantForm.company_name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="联系人" prop="contacts">
            <el-input v-model="merchantForm.contacts" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="支付类型" prop="pay_type">
            <el-select v-model="merchantForm.pay_type" style="width: 100%;" placeholder="请选择支付类型">
              <el-option label="微信" :value="1"></el-option>
              <el-option label="支付宝" :value="2"></el-option>
              <el-option label="银行卡" :value="3"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="费率" prop="rate">
            <el-input v-model="merchantForm.rate" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="appid" prop="appid">
            <el-input v-model="merchantForm.appid" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="appkey" prop="appkey">
            <el-input v-model="merchantForm.appkey" auto-complete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="resetForm('merchantForm')">取 消</el-button>
          <el-button type="primary" @click="submitForm('merchantForm')">确 定</el-button>
        </div>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
import merchant from '../../api/config/merchant'

import { filterMerchantStatus, filterMerchantPayType } from '../../filters'

export default {
  data () {
    return {
      loading: false,
      merchants: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      params: {},
      merchantFormVisable: false,
      merchantForm: {
        company_name: '',
        pay_type: 1,
        rate: 0,
        appid: '',
        appkey: ''
      },
      merchantRule: {
        company_name: [
          { required: true, message: '请输入公司名称', trigger: 'blur' }
        ],
        contacts: [
          { required: true, message: '请输入联系人', trigger: 'blur' }
        ],
        pay_type: [
          { required: true, message: '请选择支付类型', trigger: 'blur' }
        ],
        rate: [
          { required: true, message: '请输入支付费率', trigger: 'blur' }
        ],
        appid: [
          { required: true, message: '请输入appid', trigger: 'blur' }
        ],
        appkey: [
          { required: true, message: '请输入appkey', trigger: 'blur' }
        ]
      },
      formTitle: '添加支付商',
      formAction: 'create'
    }
  },
  created () {
    this.init(this.$route)
    this.list(this.params)
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
      this.total = this.currentPage * 10
    },
    list (params) {
      this.loading = true
      merchant.list(params).then((data) => {
        this.merchants = data.results
        this.total = data.count
        this.loading = false
      })
    },
    handleAdd () {
      this.merchantForm = {}
      this.formTitle = '添加支付商'
      this.formAction = 'create'
      this.merchantFormVisable = true
    },
    handleEdit (id) {
      this.formTitle = '编辑支付商'
      this.formAction = 'update'
      merchant.retrieve(id).then((data) => {
        this.merchantFormVisable = true
        this.merchantForm = data
      })
    },
    handleDelete (id) {
      this.$confirm('此操作将永久删除该支付商, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        merchant.destory(id).then((data) => {
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
          let data = this.merchantForm
          if (this.formAction === 'create') {
            merchant.create(data).then((data) => {
              this.merchantFormVisable = false
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
            let id = this.merchantForm.id
            merchant.update(id, data).then((data) => {
              this.merchantFormVisable = false
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
      this.merchantFormVisable = false
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.params['page'] = val
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'PayMerchant', query: params })
    }
  },
  filters: {
    filterMerchantStatus,
    filterMerchantPayType
  },
  watch: {
    $route: {
      deep: true,
      handler: function (val) {
        if (val.name === 'ConfigMerchant') {
          this.init(val)
          this.list(this.params)
        }
      }
    }
  }
}
</script>
