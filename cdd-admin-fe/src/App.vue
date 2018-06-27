<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<style>
html, body {
  margin: 0;
  height: 100%;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
}
ul {
  margin: 0;
}
a {
  color: #4098F7;
  cursor: pointer;
  font-weight: bold;
}
.card {
  cursor: pointer;
  color: rgba(0,0,0,.45);
  font-size: 14px;
}
.card span {
  margin-left: 5px;
  margin-right: 5px;
  font-size: 36px;
  font-weight: bold;
}
.card-header {
  position: relative;
  overflow: hidden;
  width: 100%;
}
.card-header .meta {
  float: left;
}
.card-header .meta .analysis-label {
  text-align: left;
}
.card-header .meta .analysis-total {
  overflow: hidden;
  text-overflow: ellipsis;
  word-break: break-all;
  white-space: nowrap;
  color: rgba(0,0,0,.85);
  margin-top: 4px;
  margin-bottom: 0;
  font-size: 30px;
  line-height: 38px;
  height: 38px;
}
.card-header .platform {
  margin-left: 10px;
  padding-top: 37px;
  float: left;
}
.card-header .platform span {
  margin-right: 20px;
  font-size: 14px;
  color: rgba(0,0,0,.85);
}
.card-content {
  height: 46px;
  margin-bottom: 12px;
  position: relative;
  width: 100%;
}
.card-content .fixed {
  text-align: left;
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
}
.card-content .fixed span {
  margin-right: 20px;
  font-size: 14px;
  color: rgba(0,0,0,.85);
}
.card-footer {
  text-align: left;
  border-top: 1px solid #e8e8e8;
  padding-top: 9px;
  margin-top: 8px;
}
.card-footer span {
  margin-right: 20px;
  font-size: 14px;
  color: rgba(0,0,0,.85);
}
h4 {
  text-align: left;
  margin-top: 0;
  margin-bottom: .5em;
  color: rgba(0,0,0,.85);
  font-weight: 500;
}
.statistic-label {
  height: 33px;
  line-height: 35px;
  float: left;
  margin-right: 30px;
}
.statistic-span {
  font-size: 24px;
  font-weight: bold;
}
.analysis-total {
  text-align: left;
}
.filter {
  text-align: left;
}
.search-btn {
  margin-left: 20px;
}
.add-btn {
  float: right;
}
.el-table .warning-row {
  background: oldlace;
}
</style>
