<template>
  <div>
    <el-dialog
      title="被邀请人列表"
      :visible.sync="visible">
      <el-table
        :data="invitees"
        border>
        <el-table-column
          header-align="center"
          prop="id"
          label="用户ID">
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="phone_number"
          label="手机">
        </el-table-column>
        <el-table-column
          header-align="center"
          label="平台">
          <template slot-scope="scope">
            {{ scope.row.platform | filterPlatform }}
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          label="状态">
          <template slot-scope="scope">
            <el-tag
              size="mini"
              :type="handleStatusTagType(scope.row.status)">{{ scope.row.status | filterUserStatus }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          header-align="center"
          prop="reg_time"
          label="注册时间"
          width="180">
        </el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
        <el-button @click="visible = false">关 闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import user from '../../api/user'

import { filterPlatform, filterUserStatus } from '../../filters'

export default {
  data () {
    return {
      visible: false,
      invitees: []
    }
  },
  methods: {
    show (inviterID) {
      let params = {
        'inviter_id': inviterID
      }
      user.list(params).then((data) => {
        this.visible = true
        this.invitees = data.results.data
      })
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
    filterPlatform,
    filterUserStatus
  }
}
</script>
