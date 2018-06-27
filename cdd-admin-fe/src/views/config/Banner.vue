<template>
  <div v-loading="loading">
    <el-card>
      <el-row style="text-align: right;">
        <el-button size="small" @click="handleAdd" ><i class="el-icon-plus"></i> 添加Banner</el-button>
      </el-row>
      <br>
      <el-table
        :data="banners"
        style="width:100%;">
        <el-table-column
          header-align="center"
          type="index"
          width="80">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="banner_theme"
          label="主题">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="类型">
          <template slot-scope="scope">
            {{ scope.row.banner_type | filterType }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="展示状态">
          <template slot-scope="scope">
            {{ scope.row.banner_status | filterStatus }}
          </template>
        </el-table-column>
         <el-table-column
          header-align="center"
          label="主题图片">
          <template slot-scope="scope">
            <img :src="scope.row.img_url" class="theme-img" />
          </template>
        </el-table-column>
         <el-table-column
          header-align="center"
          label="目标网页">
          <template slot-scope="scope">
            <a :href="scope.row.target_url">链接</a>
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="添加时间">
          <template slot-scope="scope">
            {{ scope.row.add_time }}
          </template>
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
        :visible.sync="bannerFormVisable"
        :show-close="false"
        :close-on-press-escape="false"
        :close-on-click-modal="false">
        <div slot="title">
          {{ formTitle }}
        </div>
        <el-form :model="bannerForm" :rules="bannerRule" ref="bannerForm" label-width="120px">
          <el-form-item label="主题">
            <el-input v-model="bannerForm.banner_theme" placeholder="请输入主题" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="描述">
            <el-input v-model="bannerForm.banner_desc" placeholder="请输入描述" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="类型">
            <el-select v-model="bannerForm.banner_type" style="width: 100%;" placeholder="请选择类型">
              <el-option v-for="item in typeData" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="bannerForm.banner_status" style="width: 100%;" placeholder="请选择状态">
              <el-option v-for="item in statusData" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="图片">
            <el-upload
              :data="uploadData()"
              :action="uploadFileURL()"
              :headers="setHeaders()"
              :on-success="handleUploadSuccess"
              :on-error="handleUploadError"
              :on-exceed="handleImageExceed"
              :file-list="imageList"
              list-type="picture">
              <el-button size="small" type="primary">点击上传</el-button>
              <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
            </el-upload>
          </el-form-item>
          <el-form-item label="网页URL">
            <el-input v-model="bannerForm.target_url" placeholder="网页URL" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="活动URL">
            <el-input v-model="bannerForm.target_activity" placeholder="活动URL" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="活动参数">
            <el-input v-model="bannerForm.target_args" placeholder="活动参数" auto-complete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="resetForm('bannerForm')">取 消</el-button>
          <el-button type="primary" @click="submitForm('bannerForm')">确 定</el-button>
        </div>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
import banner from '../../api/config/banner'
import { API_ROOT } from '../../config'
import user from '../../localStorage/user'

export default {
  data () {
    return {
      loading: false,
      banners: [],
      currentPage: 1,
      pageSize: 10,
      total: 0,
      typeData: [{
        value: 1,
        label: '网址'
      }, {
        value: 2,
        label: 'app'
      }],
      statusData: [{
        value: 0,
        label: '下线'
      }, {
        value: 1,
        label: '上线'
      }],
      imageList: [],
      bannerForm: {
        banner_theme: '',
        banner_desc: '',
        banner_type: '',
        banner_status: '',
        img_url: '',
        target_url: '',
        target_activity: '',
        target_args: ''
      },
      bannerRule: {},
      bannerFormVisable: false,
      params: {},
      formTitle: '添加banner',
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
      banner.list(params).then((data) => {
        this.banners = data.results
        this.total = data.count
        this.loading = false
      })
    },
    handleUploadSuccess (response, file, fileList) {
      this.bannerForm.img_url = response.data.url
      this.imageList = [{url: response.data.url}]
    },
    handleUploadError (file, fileList) {
      this.$message({
        type: 'warning',
        message: '上传失败'
      })
    },
    handleImageExceed (file) {
      this.$message({
        type: 'warning',
        message: '只能上传1张图片!'
      })
    },
    handleAdd () {
      this.bannerForm = {}
      this.formTitle = '添加Banner'
      this.formAction = 'create'
      this.bannerFormVisable = true
      this.imageList = []
    },
    handleEdit (id) {
      this.formTitle = '编辑Banner'
      this.formAction = 'update'
      banner.retrieve(id).then((data) => {
        this.bannerFormVisable = true
        this.bannerForm = data
        this.imageList = [{url: data.img_url}]
      })
    },
    handleDelete (id) {
      this.$confirm('此操作将永久删除该Banner, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        banner.destory(id).then((data) => {
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
          let data = this.bannerForm
          if (this.formAction === 'create') {
            banner.create(data).then((data) => {
              this.bannerFormVisable = false
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
            let id = this.bannerForm.id
            banner.update(id, data).then((data) => {
              this.bannerFormVisable = false
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
          }
        }
      })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
      this.bannerFormVisable = false
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.params['page'] = val
      let params = Object.assign({}, this.params)
      this.$router.push({ name: 'ConfigBanner', query: params })
    },
    uploadFileURL () {
      return `${API_ROOT}/api/upload/`
    },
    uploadData () {
      let data = {
        type: 'image'
      }
      return data
    },
    setHeaders () {
      return {
        'Authorization': `Bearer ${user.token}`
      }
    }
  },
  filters: {
    filterStatus (val) {
      let dictStatus = {
        0: '已下线',
        1: '已上线'
      }
      return dictStatus[val]
    },
    filterType (val) {
      let dictType = {
        1: '网址',
        2: 'app'
      }
      return dictType[val]
    }
  },
  watch: {
    $route: {
      deep: true,
      handler: function (val) {
        if (val.name === 'ConfigBanner') {
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
