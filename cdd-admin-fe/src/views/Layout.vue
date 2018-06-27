<template>
  <div style="height: 100%">
    <el-container style="height: 100%;">
      <el-aside width="260px" class="hidden-xs-only">
        <el-menu style="height: 100%; text-align: left;"
          :default-active="activeIndex"
          unique-opened
          mode="vertical"
          background-color="#494F5E"
          text-color="#fff"
          active-text-color="#ffd04b"
          :router="true">
          <div class="logo">
            彩多多
          </div>
          <div v-for="(item, index) in layout_list" :key="index">
            <el-menu-item v-if="item.children.length <= 0" :key="item.id" :index="item.url">{{ item.name }}</el-menu-item>
            <el-submenu v-else :index="item.url" :key="item.id" >
              <template slot="title">{{ item.name }}</template>
              <el-menu-item v-for="child in item.children" :key="child.id" :index="child.url">{{ child.name }}</el-menu-item>
            </el-submenu>
          </div>
           <el-menu-item index="/admin">管理员列表</el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header>
          <!-- <div class="search" v-if="user.role === 'commerce'">
            <el-input size="small" v-model="keyword" placeholder="请输入关键字" class="input-with-select">
              <el-select v-model="lottery" slot="prepend" placeholder="请选择">
                <el-option label="数字彩" value="number"></el-option>
                <el-option label="竞技彩" value="sports"></el-option>
              </el-select>
              <el-button slot="append" icon="el-icon-search" @click="handleSearch"></el-button>
            </el-input>
          </div> -->
          <div class="profile">
            <el-dropdown @command="handleCommand">
              <span class="el-dropdown-link">
                账户<i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="ChangePassword" v-if="user.role !== 'commerce'">
                  修改密码
                </el-dropdown-item>
                <el-dropdown-item command="Logout">
                  退出
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
        </el-header>
        <el-main>
          <router-view/>
        </el-main>
        <el-footer>
          <div class="copyright">
            2018 &copy; 数字生活
          </div>
        </el-footer>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import user from '../localStorage/user'
import layout from '../api/layout'

export default {
  name: 'Layout',
  data () {
    return {
      activeIndex: '/',
      user: {},
      lottery: '',
      keyword: '',
      layout_list: []
    }
  },
  created () {
    this.activeIndex = this.$route.path
    this.user = user
    this.list(this.params)
  },
  methods: {
    list (params) {
      layout.listLayout(params).then((data) => {
        this.layout_list = data
      })
    },
    handleSearch () {
      if (this.keyword && this.lottery) {
        let query = {
          keyword: this.keyword
        }
        if (this.lottery === 'number') {
          this.$router.push({ name: 'SearchNumber', query: query })
        } else {
          this.$router.push({ name: 'SearchSports', query: query })
        }
      } else {
        this.$message({
          type: 'warning',
          message: '请选择彩种并输入关键字'
        })
      }
    },
    handleCommand (name) {
      this.$router.push({ name: name })
    }
  }
}
</script>

<style>
.logo {
  height: 60px;
  line-height: 60px;
  font-size: 30px;
  font-weight: bold;
  color: #fff;
  background-color: #3A404A;
  text-align: center;
}
.el-header {
  padding: 0;
  border-bottom: 1px solid #ebeef5;
  box-shadow: 0 0 12px 0 rgba(0,0,0,.1);
}
.search {
  float: left;
  width: 30%;
  margin-left: 20px;
  line-height: 61px;
}
.search:focus {
  outline: none;
}
.profile {
  float: right;
  width: 80px;
  margin-right: 20px;
  line-height: 61px;
  cursor: pointer;
}
.profile:hover {
  background-color: #E7F7FE;
}
.profile span:focus {
  outline: none;
}
.el-select .el-input {
  width: 130px;
}
.input-with-select .el-input-group__prepend {
  background-color: #fff;
}
.copyright {
  height: 60px;
  line-height: 60px;
}
</style>
