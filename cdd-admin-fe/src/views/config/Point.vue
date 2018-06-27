<template>
  <div v-loading="loading">
    <el-card>
      <el-row class="add-btn">
        <el-button size="small" @click="handleAdd"><i class="el-icon-plus"></i> 添加埋点</el-button>
      </el-row>
      <br />
      <el-table
        :data="points"
        style="width: 100%">
        <el-table-column
          header-align="center"
          type="index"
          width="80">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="id"
          label="编号">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="name"
          label="名称">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="description"
          label="描述">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="created_at"
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
      <el-dialog :visible.sync="pointFormVisable" :show-close="false" :close-on-press-escape="false" :close-on-click-modal="false">
        <div slot="title">
          {{ formTitle }}
        </div>
        <el-form :model="pointForm" :rules="pointRule" ref="pointForm" label-width="120px">
          <el-form-item label="名称" prop="name">
            <el-input v-model="pointForm.name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="描述" prop="description">
            <el-input v-model="pointForm.description" auto-complete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="resetForm('pointForm')">取 消</el-button>
          <el-button type="primary" @click="submitForm('pointForm')">确 定</el-button>
        </div>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
import point from '../../api/config/point'

export default {
  data () {
    return {
      loading: false,
      points: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      params: {},
      pointFormVisable: false,
      pointForm: {
        name: '',
        description: ''
      },
      pointRule: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '请输入描述', trigger: 'blur' }
        ]
      },
      formTitle: '添加点位',
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
      this.total = this.currentPage * 10
    },
    list (params) {
      this.loading = true
      point.list(params).then((data) => {
        this.points = data.results
        this.total = data.count
        this.loading = false
      })
    },
    handleAdd () {
      this.pointForm = {}
      this.formTitle = '添加点位'
      this.formAction = 'create'
      this.pointFormVisable = true
    },
    handleEdit (id) {
      this.formTitle = '编辑点位'
      this.formAction = 'update'
      point.retrieve(id).then((data) => {
        this.pointFormVisable = true
        this.pointForm = data
      })
    },
    handleDelete (id) {
      this.$confirm('此操作将永久删除该点位, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        point.destory(id).then((data) => {
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
          let data = this.pointForm
          if (this.formAction === 'create') {
            point.create(data).then((data) => {
              this.pointFormVisable = false
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
            let id = this.pointForm.id
            point.update(id, data).then((data) => {
              this.pointFormVisable = false
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
      this.pointFormVisable = false
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.params['page'] = val
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'Point', query: params })
    }
  },
  watch: {
    $route: {
      deep: true,
      handler: function (val) {
        if (val.name === 'ConfigPoint') {
          this.init(val)
          this.list(this.params)
        }
      }
    }
  }
}
</script>
