<template>
  <div class="case">
    <div style="text-align: left; margin-top: 20px;">
      <el-form :inline="true">
        <el-form-item label="项目">
          <el-select
            v-model="projectValue"
            size="medium"
            placeholder="请选择项目"
            @change="changeProject()"
          >
            <el-option
              v-for="(item, index) in projectOption"
              :key="index"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="small" @click="syncProject">同步</el-button>
        </el-form-item>
        <el-form-item label="用例" style="float: right;">
          <el-tag>{{ caseNumber }}</el-tag> 条
        </el-form-item>
        <el-form-item label="环境" style="float: right;">
          <el-select v-model="env" placeholder="请选择执行环境" size="small">
            <el-option
              v-for="item in envOptions"
              :key="item.vaule"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item style="float: right;">
          <el-button type="primary" size="small" @click="showDialog()">创建环境</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div style="height: 60px; margin-top: 10px;">
      <span> 用例列表</span>
      <span style="float: right">
        <el-button v-if="fullName != ''" type="success" size="mini" @click="initFileCases()">刷新</el-button>
      </span>
    </div>
    <div style="min-height: 650px;">
      <div class="case-dir-tree">
        <div style="width: 100%; height: 600px;">
          <el-scrollbar style="height:100%">
            <el-tree
              ref="tree"
              :data="fileData"
              node-key="id"
              lazy
              :props="defaultProps"
              @node-expand="handleNodeClick"
            >
              <span slot-scope="{ node, data }">
                <span v-if="data.is_leaf === 1">
                  <i class="el-icon-tickets" />
                </span>
                <span v-else>
                  <i class="el-icon-folder" />
                </span>
                {{ data.label }}
              </span>
            </el-tree>
          </el-scrollbar>
        </div>
      </div>
      <div style="width: 78%; float: right">
        <el-table :data="caseData" border style="width: 100%" height="600" @row-click="caseRowClick">
          <el-table-column prop="id" label="ID" width="100" />
          <el-table-column prop="class_name" label="测试类" />
          <el-table-column prop="class_doc" label="测试类描述" />
          <el-table-column prop="case_name" label="测试方法" />
          <el-table-column prop="case_doc" label="测试方法描述" />
          <el-table-column prop="status" label="状态">
            <template slot-scope="scope">
              <span v-if="scope.row.status === 0">
                <el-tag type="info"> 未执行 </el-tag>
              </span>
              <span v-else-if="scope.row.status === 1">
                <el-tag type="success"> 执行中 </el-tag>
              </span>
              <span v-else-if="scope.row.status === 2">
                <el-tag> 已执行 </el-tag>
              </span>
              <span v-else>
                <el-tag type="danger"> 未知 </el-tag>
              </span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120">
            <template slot-scope="scope">
              <el-button type="success" size="mini" @click="runCase(scope.row)" @click.stop="drawer = false">执行</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
    <!--引入子组件-->
    <env-dialog v-if="dialogFlag" :title="dialogTitle" :pid="projectValue" @cancel="closeDialog" />

    <el-drawer
      title="测试结果"
      :visible.sync="drawer"
      direction="rtl"
      size="40%"
    >
      <result-dialog v-if="drawer" :cid="caseId" @cancel="cancelDialog" />
    </el-drawer>
  </div>
</template>
<script>
import { projectList } from '@/api/projects'
import { getProjectFiles, syncProjectCase, getProjectCases, getProjectSubdirectory, runningCase } from '@/api/cases'
import { getEnvs } from '@/api/evns'
import envDialog from './components/envDialog.vue'
import resultDialog from './components/resultDialog.vue'

export default {
  name: 'CaseModule',
  components: {
    envDialog,
    resultDialog
  },
  data() {
    return {
      dialogFlag: false,
      dialogTitle: 'create',
      loading: true,
      projectValue: 1,
      projectLabel: '',
      projectOption: [],
      caseId: '',
      caseNumber: 0,
      fullName: '',
      fileData: [],
      caseData: [],
      defaultProps: {
        children: 'children',
        label: 'label'
      },
      env: '',
      envOptions: [],
      drawer: false
    }
  },
  mounted() {
    this.initProjectList()
  },
  methods: {
    // 初始化项目列表
    async initProjectList() {
      const resp = await projectList(this.req)
      if (resp.success === true) {
        this.projectValue = resp.items[0].id
        this.projectLabel = resp.items[0].name
        for (let i = 0; i < resp.items.length; i++) {
          this.projectOption.push({
            value: resp.items[i].id,
            label: resp.items[i].name
          })
        }
        this.initProjectFile()
        this.initEnv(this.projectValue)
        // this.$message.success("查询成功！")
      } else {
        this.$message.error('查询失败！')
      }
    },

    // 初始化项目文件列表
    async initProjectFile() {
      const resp = await getProjectFiles(this.projectValue)
      if (resp.success === true) {
        this.fileData = resp.data.files
        this.caseNumber = resp.data.case_number
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 初始化环境列表
    async initEnv(pid) {
      const resp = await getEnvs(pid)
      if (resp.success === true) {
        // 进行push前重置 envOptions 内容
        this.envOptions = []
        for (let i = 0; i < resp.data.length; i++) {
          this.envOptions.push({
            value: resp.data[i].id,
            label: resp.data[i].name
          })
        }
      } else {
        this.$message.error(resp.error.message)
      }
    },

    changeProject() {
      this.initProjectFile()
      this.initEnv(this.projectValue)
    },

    // 同步项目用例
    async syncProject() {
      if (this.projectId === '') {
        this.$message.error('请选择项目')
        return
      }
      const resp = await syncProjectCase(this.projectValue)
      if (resp.success === true) {
        this.initProjectFile()
        this.$message.success('同步成功')
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 获得文件用例
    initFileCases() {
      const req = { file_name: this.fullName }
      getProjectCases(this.projectValue, req).then(resp => {
        if (resp.success === true) {
          // this.$message.success('获取用例列表成功')
          this.caseData = resp.data
        } else {
          this.$message.error(resp.error.message)
        }
      })
    },

    // 点击tree节点
    handleNodeClick(data) {
      // 如果是文件返回 类&方法
      if (data.label.match('.py')) {
        this.fullName = data.full_name
        this.initFileCases()
      } else {
        // 如果目录返回下一级 目录&文件
        if (data.children.length > 0) {
          // 下一级不为空，直接返回
          return
        }
        const req = { file_name: data.full_name }
        getProjectSubdirectory(this.projectValue, req).then(resp => {
          if (resp.success === true) {
            data.children = resp.data
          } else {
            this.$message.error(resp.error.message)
          }
        })
      }
    },
    caseRowClick(row) {
      this.caseId = row.id
      this.drawer = true
    },
    // 展示子组件
    showDialog() {
      this.dialogTitle = 'create'
      this.dialogFlag = true
    },
    // 关闭子组件，子组件的closeDialog回调父组件
    closeDialog() {
      this.dialogFlag = false
      this.initEnv(this.projectValue)
      this.initProjectFile()
    },
    // 运行用例
    async runCase(row) {
      if (this.env === '') {
        this.$message.error('请选择运行环境')
        return
      }
      const resp = await runningCase(row.id, { env: this.env })
      if (resp.success === true) {
        this.$message.success('开始执行')
      } else {
        this.$message.error('运行失败')
      }
    },
    // 打开报告
    openReport(row) {
      window.open('/reports/' + row.report)
    },
    // 子组件的回调
    cancelDialog() {
      this.drawer = false
    }
  }
}
</script>
  <style scoped>
  .custom-tree-node {
    width: 100%;
  }
  .el-card-define {
    height: 720px;
  }
  /* 定义当前组件使用的CSS */
.case-dir-tree {
  width: 21%;
  float: left;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)
}
  </style>
