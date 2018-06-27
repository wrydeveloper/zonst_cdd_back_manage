<template>
  <div v-loading="loading">
    <el-card>
      <el-row class="add-btn">
        <el-button size="small" @click="handleAdd"><i class="el-icon-plus"></i> 添加商务</el-button>
      </el-row>
      <br />
      <el-table
        :data="commerces"
        style="width: 100%">
        <el-table-column
          header-align="center"
          type="index"
          width="80">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="bd_id"
          label="商务工号">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="bd_name"
          label="商务姓名">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="状态">
          <template slot-scope="scope">
            <el-tag
              size="mini"
              :type="handleStatusTagType(scope.row.status)">{{ scope.row.status | filterStatus }}
            </el-tag>
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
          align="center">
          <template slot-scope="scope">
            <el-button size="mini" @click="handleEdit(scope.row.id)">编辑</el-button>
            <!-- <el-button type="danger" size="mini" @click="handleDelete(scope.row.id)">删除</el-button> -->
            <el-button type="primary" size="mini" @click="goProxy(scope.row.id)">代理列表</el-button>
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
        :visible.sync="commerceFormVisable"
        :show-close="false"
        :close-on-press-escape="false"
        :close-on-click-modal="false">
        <div slot="title">
          {{ formTitle }}
        </div>
        <el-form :model="commerceForm" :rules="customerRule" ref="commerceForm" label-width="120px">
          <el-form-item label="商务工号" prop="bd_id">
            <el-input v-model="commerceForm.bd_id" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="商务姓名" prop="bd_name">
            <el-input v-model="commerceForm.bd_name" auto-complete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="resetForm('commerceForm')">取 消</el-button>
          <el-button type="primary" @click="submitForm('commerceForm')">确 定</el-button>
        </div>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
import commerce from '../../api/commerce'

export default {
  data () {
    return {
      loading: false,
      commerces: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      params: {},
      keyword: '',
      commerceFormVisable: false,
      commerceForm: {
        'bd_id': '',
        'bd_name': ''
      },
      customerRule: {
        bd_id: [
          { required: true, message: '请输入商务工号', trigger: 'blur' }
        ],
        bd_name: [
          { required: true, message: '请输入商务姓名', trigger: 'blur' }
        ]
      },
      formTitle: '添加商务',
      formAction: 'create',
      btnSearchState: true
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
      commerce.list(params).then((data) => {
        this.commerces = data.results
        this.total = data.count
        this.loading = false
      })
    },
    handleAdd () {
      this.commerceForm = {}
      this.formTitle = '添加商务'
      this.formAction = 'create'
      this.commerceFormVisable = true
    },
    handleEdit (id) {
      this.formTitle = '编辑商务'
      this.formAction = 'update'
      commerce.retrieve(id).then((data) => {
        this.commerceFormVisable = true
        this.commerceForm = data
      })
    },
    handleDelete (id) {
      this.$confirm('此操作将永久删除该商务, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        commerce.destory(id).then((data) => {
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
          let data = this.commerceForm
          if (this.formAction === 'create') {
            commerce.create(data).then((data) => {
              this.commerceFormVisable = false
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
            let id = this.customerForm.id
            commerce.update(id, data).then((data) => {
              this.commerceFormVisable = false
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
      this.commerceFormVisable = false
    },
    goProxy (bdID) {
      let query = {
        bd_id: bdID
      }
      this.$router.push({ name: 'PromotionProxy', query: query })
    },
    handleSearch () {
      if (this.keyword !== '') {
        this.params['keyword'] = this.keyword
      }
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'PromotionCommerce', query: params })
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.params['page'] = val
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'PromotionCommerce', query: params })
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
    filterStatus (val) {
      if (val === 1) {
        return '已启用'
      } else {
        return '已禁用'
      }
    }
  },
  watch: {
    keyword: function (val) {
      if (val !== '') {
        this.btnSearchState = false
      } else {
        this.btnSearchState = true
      }
    },
    $route: {
      deep: true,
      handler: function (val) {
        if (val.name === 'PromotionCommerce') {
          this.init(val)
          this.list(this.params)
        }
      }
    }
  }
}
</script>
