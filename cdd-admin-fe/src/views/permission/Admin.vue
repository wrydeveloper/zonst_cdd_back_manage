<template>
    <div v-loading="loading">
    <el-card>
      <el-table
        :data="admins"
        style="width: 100%">
        <el-table-column
          header-align="center"
          type="index"
          width="80">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="name"
          label="管理员号码">
        </el-table-column>
        <el-table-column
          prop="role_name"
          header-align="center"
          label="管理员角色">
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
            <el-button size="mini" @click="handleEdit(scope.row.id, scope.row.role_id)">编辑</el-button>
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
        :visible.sync="adminFormVisable"
        :show-close="false"
        :close-on-press-escape="false"
        :close-on-click-modal="false">
        <div slot="title">
          角色设置
        </div>
        <el-form :model="adminForm" ref="adminForm" label-width="120px">
          <el-form-item label="角色选择" prop="rold_id">
            <el-select v-model="adminForm.role_id" placeholder="请选择角色" clearable>
              <el-option v-for="item in roleData" :key="item.id" :label="item.name" :value="item.id"></el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="resetForm('adminForm')">取 消</el-button>
          <el-button type="primary" @click="submitForm('adminForm')">立刻设置</el-button>
        </div>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
import admin from '../../api/admin'
import role from '../../api/role'

export default {
  data () {
    return {
      loading: false,
      admins: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      params: {},
      adminFormVisable: false,
      nowAdminId: 0,
      adminForm: {
        'role_id': 0
      },
      roleData: []
    }
  },
  created () {
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
      admin.listAdminData(params).then((data) => {
        this.admins = data.results
        this.total = data.count
        this.loading = false
      })
      role.list(params).then((data) => {
        this.roleData = data.results
      })
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.params['page'] = val
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'Admin', query: params })
    },
    handleStatusTagType (val) {
      if (val === 1) {
        return 'success'
      } else {
        return 'danger'
      }
    },
    resetForm (formName) {
      this.adminFormVisable = false
    },
    submitForm (formName) {
      let id = this.nowAdminId
      let data = this.adminForm
      admin.updateAdminRoleSetting(id, data).then((data) => {
        this.adminFormVisable = false
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
    },
    handleEdit (id, roleId) {
      this.adminForm.role_id = ''
      if (roleId !== 0) {
        this.adminForm.role_id = roleId
      }
      this.nowAdminId = id
      this.adminFormVisable = true
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
  }
}
</script>
