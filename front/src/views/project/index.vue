<template>
  <div class="project">
    <div style="height: 50px; text-align: left; width: 100%; margin-top: 20px;">
      <el-button type="primary" @click="showDialog()">创建</el-button>
    </div>

    <div style="height: 700px">
      <div
        v-for="(item, index) in projectData"
        :key="index"
        class="text item"
      >
        <el-col :span="7" class="project-card">
          <el-card style="width: 350px; margin-top:20px">
            <div slot="header" class="clearfix">
              <span>{{ item.name }}</span>
              <div style="float: right">
                <el-dropdown>
                  <span class="el-dropdown-link">
                    <i class="el-icon-setting" />
                  </span>
                  <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item>
                      <el-button
                        type="text"
                        @click="cloneProject(item.id)"
                      >克隆</el-button>
                    </el-dropdown-item>
                    <el-dropdown-item>
                      <el-button
                        type="text"
                        @click="showDetail(item.id)"
                      >详情</el-button>
                    </el-dropdown-item>
                    <el-dropdown-item>
                      <el-button
                        type="text"
                        @click="showEdit(item.id)"
                      >编辑</el-button>
                    </el-dropdown-item>
                    <el-dropdown-item>
                      <el-button
                        type="text"
                        @click="deleteProject(item.id)"
                      >删除</el-button>
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>
              </div>
            </div>
            {{ item.address }}
            <img
              :src="item.image"
              class="image"
              style="height: 235px; width: 310px"
            >
          </el-card>
        </el-col>
      </div>
    </div>
    <!--分页-->
    <div style="width: 100%; text-align: right">
      <el-pagination
        background
        layout="prev, pager, next"
        :page-size="req.size"
        :total="total"
        @current-change="handleCurrentChange"
      />
    </div>
    <!--引入子组件-->
    <project-dialog
      v-if="dialogFlag"
      :title="dialogTitle"
      :pid="currentPorjectId"
      @cancel="closeDialog"
    />
  </div>
</template>

<script>
import ProjectDialog from './components/projectDialog.vue'
import { projectList, deleteProject, cloneProject } from '@/api/projects'

export default {
  name: 'Porject',
  components: {
    ProjectDialog
  },
  data() {
    return {
      dialogFlag: false,
      dialogTitle: 'create',
      currentPorjectId: 0,
      projectData: [],
      req: {
        page: 1,
        size: 6
      },
      // 分页页数
      total: 10
    }
  },
  mounted() {
    // 组件加载的时候 进行调用
    this.initProjectList()
  },
  methods: {
    async initProjectList() {
      const resp = await projectList(this.req)
      if (resp.success === true) {
        // 处理加载的图片路径
        for (let i = 0; i < resp.items.length; i++) {
          resp.items[i].image = '/static/images/' + resp.items[i].image
        }
        this.projectData = resp.items
        this.total = resp.total
        // this.$message.success('查询成功！')
      } else {
        this.$message.error('查询失败！')
      }
    },
    // 展示子组件
    showDialog() {
      this.dialogTitle = 'create'
      this.dialogFlag = true
    },
    // 关闭子组件，子组件的closeDialog回调父组件
    closeDialog() {
      this.dialogFlag = false
      this.initProjectList()
    },
    // 跳转到第几页
    handleCurrentChange(val) {
      // console.log(`当前页: ${val}`)
      this.req.page = val
      this.initProjectList()
    },
    // 展示项目详情
    showDetail(id) {
      this.currentPorjectId = id
      this.dialogTitle = 'detail'
      this.dialogFlag = true
    },
    // 编辑项目
    showEdit(id) {
      this.currentPorjectId = id
      this.dialogTitle = 'edit'
      this.dialogFlag = true
    },
    // 克隆项目
    async cloneProject(id) {
      const resp = await cloneProject(id)
      console.info('克隆项目')
      if (resp.success === true) {
        this.$message.success('项目克隆成功！')
      } else {
        this.$message.error('项目克隆失败！')
      }
    },
    // 删除项目
    async deleteProject(id) {
      await deleteProject(id).then((resp) => {
        this.$confirm('删除任务, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          center: true
        }).then(() => {
          if (resp.success === true) {
            this.initProjectList()
          } else {
            this.$message.error(resp.error.msg)
          }
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
      })
    }
  }
}
</script>
