<template>
  <div v-loading="loading">
    <el-card>
      <el-row class="add-btn">
        <el-button size="small" @click="handleAdd"><i class="el-icon-plus"></i> 添加支付渠道</el-button>
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
          prop="channel_id"
          label="渠道ID">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="channel_name"
          label="渠道名称">
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
        :visible.sync="channelFormVisable"
        :show-close="false"
        :close-on-press-escape="false"
        :close-on-click-modal="false">
        <div slot="title">
          {{ formTitle }}
        </div>
        <el-form :model="channelForm" :rules="channelRule" ref="channelForm" label-width="120px">
          <el-form-item label="渠道号" prop="channel_id">
            <el-input v-model="channelForm.channel_id" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="渠道名" prop="channel_name">
            <el-input v-model="channelForm.channel_name" auto-complete="off"></el-input>
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
import channel from '../../api/config/channel'

export default {
  data () {
    return {
      loading: false,
      channels: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      params: {},
      channelFormVisable: false,
      channelForm: {
        channel_id: '',
        channel_name: ''
      },
      channelRule: {
        channel_id: [
          { required: true, message: '请输入渠道号', trigger: 'blur' }
        ],
        channel_name: [
          { required: true, message: '请输入渠道名', trigger: 'blur' }
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
      channel.list(params).then((data) => {
        this.channels = data.results
        this.total = data.count
        this.loading = false
      })
    },
    handleAdd () {
      this.channelForm = {}
      this.formTitle = '添加支付渠道'
      this.formAction = 'create'
      this.channelFormVisable = true
    },
    handleEdit (id) {
      this.formTitle = '编辑支付渠道'
      this.formAction = 'update'
      channel.retrieve(id).then((data) => {
        this.channelFormVisable = true
        this.channelForm = data
      })
    },
    handleDelete (id) {
      this.$confirm('此操作将永久删除该支付渠道, 是否继续?', '提示', {
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
    handleCurrentChange (val) {
      this.currentPage = val
      this.params['page'] = val
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'ConfigChannel', query: params })
    }
  },
  watch: {
    $route: {
      deep: true,
      handler: function (val) {
        if (val.name === 'ConfigChannel') {
          this.init(val)
          this.list(this.params)
        }
      }
    }
  }
}
</script>
