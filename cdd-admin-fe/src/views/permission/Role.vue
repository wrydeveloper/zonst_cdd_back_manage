<template>
  <div v-loading="loading">
    <el-card>
      <el-row style="text-align: right;">
        <el-button size="small" @click="handleAdd" ><i class="el-icon-plus"></i> 添加角色</el-button>
      </el-row>
      <br>
      <el-table
        :data="roles"
        style="width:100%;">
        <el-table-column
          header-align="center"
          type="index"
          width="80">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="name"
          label="角色">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="description"
          label="描述">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="add_time"
          label="添加时间">
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
      <br/>
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
        :visible.sync="roleFormVisable"
        :show-close="false"
        :close-on-press-escape="false"
        :close-on-click-modal="false">
        <div slot="title">
          {{ formTitle }}
        </div>
        <el-form :model="roleForm" :rules="roleRule" ref="roleForm" label-width="120px">
          <el-form-item label="角色">
            <el-input v-model="roleForm.name" placeholder="请输入角色" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="描述">
            <el-input v-model="roleForm.description" placeholder="请输入描述" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="权限">
            <el-tree
              v-model="roleForm.permissions"
              :data="permissions"
              show-checkbox
              default-expand-all
              :default-checked-keys="roleForm.permissions"
              node-key="id"
              ref="tree"
              highlight-current
              :props="defaultProps">
            </el-tree>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="resetForm('roleForm')">取 消</el-button>
          <el-button type="primary" @click="submitForm('roleForm')">确 定</el-button>
        </div>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
import role from '../../api/role'
import permission from '../../api/permission'
// import user from '../../localStorage/user'

export default {
  data () {
    return {
      loading: false,
      roles: [],
      permissions: [],
      currentPage: 1,
      pageSize: 10,
      total: 0,
      roleForm: {
        name: '',
        description: '',
        permissions: []
      },
      roleRule: {},
      roleFormVisable: false,
      params: {},
      formTitle: '添加角色',
      formAction: 'create',
      defaultProps: {
        label: 'name',
        children: 'children'
      }
    }
  },
  created () {
    this.init(this.$route)
    this.list(this.params)
    this.listPermission()
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
      role.list(params).then((data) => {
        this.roles = data.results
        this.total = data.count
        this.loading = false
      })
    },
    listPermission () {
      permission.list().then((data) => {
        this.permissions = data
      })
    },
    handleAdd () {
      this.roleForm = {}
      this.formTitle = '添加角色'
      this.formAction = 'create'
      this.roleFormVisable = true
      if (this.$refs.tree) {
        this.$refs.tree.setCheckedKeys([])
      }
    },
    handleEdit (id) {
      this.formTitle = '编辑角色'
      this.formAction = 'update'
      role.retrieve(id).then((data) => {
        this.roleFormVisable = true
        this.roleForm = data
        if (this.$refs.tree) {
          this.$refs.tree.setCheckedKeys(data.permissions)
        }
      })
    },
    handleDelete (id) {
      this.$confirm('此操作将永久删除该角色, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        role.destory(id).then((data) => {
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
          let data = this.roleForm
          console.log(data)
          this.roleForm.permissions = this.$refs.tree.getCheckedKeys()
          if (this.formAction === 'create') {
            role.create(data).then((data) => {
              this.roleFormVisable = false
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
            let id = this.roleForm.id
            role.update(id, data).then((data) => {
              console.log(data)
              this.roleFormVisable = false
              this.$message({
                type: 'success',
                message: '编辑成功!'
              })
              this.list()
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
      this.roleFormVisable = false
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.params['page'] = val
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'Role', query: params })
    }
  },
  filters: {},
  watch: {
    $route: {
      deep: true,
      handler: function (val) {
        if (val.name === 'Role') {
          this.init(val)
          this.list(this.params)
        }
      }
    }
  }
}
</script>

<style>
.theme-img {
  width: 200px;
  height: 50px;
}
</style>
