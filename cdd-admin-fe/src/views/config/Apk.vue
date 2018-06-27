<template>
  <div>
    <el-card>
      <el-upload
        drag
        :action="uploadFileURL()"
        :headers="setHeaders()"
        :on-success="handleSuccess"
        multiple>
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip" slot="tip">不能超过20mb</div>
      </el-upload>
      <br>
      <el-row>
        <el-col :span="8" :offset="8">
          <el-input v-for="url in urls" :key="url" size="mini" :value="url"></el-input>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import { API_ROOT } from '../../config'
import user from '../../localStorage/user'

export default {
  data () {
    return {
      urls: []
    }
  },
  methods: {
    uploadFileURL () {
      return `${API_ROOT}/api/upload/`
    },
    setHeaders () {
      return {
        'Authorization': `Bearer ${user.token}`
      }
    },
    handleSuccess (response, file, fileList) {
      this.urls.push(response.data.url)
    }
  }
}
</script>
