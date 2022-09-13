<template>
  <div class="envs">
    <div class="filter-line" style="text-align: left; margin-top: 20px;">
      <el-button cy-data="create-project" type="primary" @click="showCreate()">创建</el-button>
    </div>
    <div class="envlist">
      <el-table :data="envData" border style="width: 100%">
        <el-table-column fixed prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="project_name" label="所属项目" />
        <el-table-column prop="base_url" label="base_url" />
        <el-table-column prop="browser" label="browser" />
        <el-table-column prop="env" label="env" />
        <el-table-column prop="update_time" label="更新时间" />
        <el-table-column fixed="right" label="操作" width="100">
          <template slot-scope="scope">
            <el-button
              type="text"
              size="small"
              @click="showEdit(scope.row)"
            >编辑</el-button>
            <el-button
              type="text"
              size="small"
              @click="deleteEnv(scope.row)"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <!--分页-->
    <div style="width: 100%; text-align: right; margin-top: 20px;">
      <el-pagination
        background
        layout="prev, pager, next"
        :page-size="req.size"
        :total="total"
        @current-change="handleCurrentChange"
      />
    </div>
    <envs-dialog v-if="showDailog" :eid="envid" @cancel="cancelEnv" />
  </div>
</template>

<script>
import { getAllEnvs, deleteEnv } from '@/api/evns'
import envsDialog from './components/envsDialog.vue'

export default ({
  components: {
    envsDialog
  },
  data() {
    return {
      loading: false,
      envData: [],
      showDailog: false,
      envid: 0,
      req: {
        page: 1,
        size: 10
      },
      // 分页页数
      total: 10
    }
  },
  mounted() {
    this.initEnvList()
  },
  methods: {
    // 初始化获取环境列表
    async initEnvList() {
      console.log('获取环境列表')
      const resp = await getAllEnvs(this.req)
      if (resp.success === true) {
        this.envData = resp.items
        this.total = resp.total
        // this.$message.success("查询成功");
      } else {
        this.$message.error('查询失败!')
      }
    },
    // 显示创建窗口
    showCreate() {
      this.showDailog = true
    },
    // 显示编辑窗口
    showEdit(obj) {
      this.envid = obj.id
      this.showDailog = true
    },
    // 子组件的回调
    cancelEnv() {
      this.showDailog = false
      this.envid = 0
      this.initEnvList()
    },
    // 删除环境信息
    async deleteEnv(obj) {
      this.envid = obj.id
      const resp = await deleteEnv(this.envid)
      if (resp.success === true) {
        this.$message.success('删除成功')
        this.initEnvList()
        this.envid = 0
      } else {
        this.$message.error('删除失败!')
      }
    }
  }
})
</script>

<style>
    .el-popover.home-popover {
      width: 70px;
      min-width: auto;
    }
</style>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* 定义当前组件使用的CSS */
.filter-line {
    height: 50px;
    text-align: left;
    margin-left: 15px;
}
.foot-page {
    margin-top: 20px;
    float: right;
    margin-bottom: 20px;
}
.project-card {
    margin-left: 15px;
    margin-right: 15px;
    margin-top: 15px;
    margin-bottom: 15px
}
</style>
