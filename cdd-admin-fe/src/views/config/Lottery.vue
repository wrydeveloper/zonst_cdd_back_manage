<template>
  <div v-loading="loading">
    <el-card>
      <el-row class="add-btn">
        <el-button size="small" @click="handleAdd"><i class="el-icon-plus"></i> 添加彩票</el-button>
      </el-row>
      <br />
      <el-table
        :data="lotteries"
        style="width: 100%">
        <el-table-column
          header-align="center"
          type="index"
          width="80">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="lottery_name"
          label="彩票名称">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="lottery_alias"
          label="彩票简称">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="彩票类型">
          <template slot-scope="scope">
            {{ scope.row.lottery_type | filterLotteryType }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="description"
          label="描述">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="状态">
          <template slot-scope="scope">
            <el-tag
              size="mini"
              :type="handleStatusTagType(scope.row.status)">{{ scope.row.status | filterLotteryStatus }}
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
      <el-dialog width="30%" :visible.sync="lotteryFormVisable" :show-close="false" :close-on-press-escape="false" :close-on-click-modal="false">
        <div slot="title">
          {{ formTitle }}
        </div>
        <el-form :model="lotteryForm" :rules="lotteryRule" ref="lotteryForm" label-width="120px">
          <el-form-item label="彩票名称" prop="lottery_name">
            <el-input v-model="lotteryForm.lottery_name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="彩票简称" prop="lottery_alias">
            <el-input v-model="lotteryForm.lottery_alias" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="彩票类型" prop="lottery_type">
            <el-input v-model="lotteryForm.lottery_type" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="描述" prop="description">
            <el-input v-model="lotteryForm.description" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="状态" prop="description">
            <el-select style="float: left;" v-model="lotteryForm.status" placeholder="请选择">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="resetForm('lotteryForm')">取 消</el-button>
          <el-button type="primary" @click="submitForm('lotteryForm')">确 定</el-button>
        </div>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
import lottery from '../../api/config/lottery'

import { filterLotteryStatus, filterLotteryType } from '../../filters'

export default {
  data () {
    return {
      loading: false,
      lotteries: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      params: {},
      lotteryFormVisable: false,
      lotteryForm: {
        lottery_name: '',
        lottery_alias: '',
        lottery_type: '',
        description: ''
      },
      lotteryRule: {},
      formTitle: '添加彩票',
      formAction: 'create',
      options: [
        {
          label: '已下线',
          value: 0
        },
        {
          label: '已上线',
          value: 1
        },
        {
          label: '已暂停',
          value: 2
        }
      ]
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
      this.total = this.currentPage * 10
    },
    list (params) {
      this.loading = true
      lottery.list(params).then((data) => {
        this.lotteries = data.results
        this.total = data.count
        this.loading = false
      })
    },
    handleAdd () {
      this.lotteryForm = {}
      this.formTitle = '添加彩票'
      this.formAction = 'create'
      this.lotteryFormVisable = true
    },
    handleEdit (id) {
      this.formTitle = '编辑彩票'
      this.formAction = 'update'
      lottery.retrieve(id).then((data) => {
        this.lotteryFormVisable = true
        this.lotteryForm = data
      })
    },
    handleDelete (id) {
      this.$confirm('此操作将永久删除该彩票, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        lottery.destory(id).then((data) => {
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
          let data = this.lotteryForm
          if (this.formAction === 'create') {
            lottery.create(data).then((data) => {
              this.lotteryFormVisable = false
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
            let id = this.lotteryForm.id
            lottery.update(id, data).then((data) => {
              this.lotteryFormVisable = false
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
      this.lotteryFormVisable = false
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.params['page'] = val
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'Lottery', query: params })
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
    filterLotteryStatus,
    filterLotteryType
  },
  watch: {
    $route: {
      deep: true,
      handler: function (val) {
        if (val.name === 'ConfigLottery') {
          this.init(val)
          this.list(this.params)
        }
      }
    }
  }
}
</script>
