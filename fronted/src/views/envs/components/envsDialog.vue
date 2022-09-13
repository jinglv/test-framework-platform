
<template>
  <div class="enviornment-dialog">
    <el-dialog :title="showTitle" :visible.sync="showStatus" width="600px" @close="cancelEnv()">
      <el-form v-if="inResize === true" ref="form" :model="form" label-width="80px">
        <el-form-item label="环境名称" prop="name">
          <el-input v-model="form.name" cy-data="enviornment-name" />
        </el-form-item>
        <el-form-item label="所属项目" prop="project">
          <el-select
            v-model="form.project_id"
            placeholder="请选择项目..."
            style="width:480px"
          >
            <el-option
              v-for="(item, index) in projectOption"
              :key="index"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="环境" prop="env">
          <el-input v-model="form.env" cy-data="enviornment-env" />
        </el-form-item>
        <el-form-item label="浏览器" prop="browser">
          <el-input v-model="form.browser" cy-data="enviornment-browser" />
        </el-form-item>
        <el-form-item label="URL" prop="base_url">
          <el-input v-model="form.base_url" cy-data="enviornment-url" />
        </el-form-item>
        <el-form-item style="margin-top: 22px; margin-bottom: 0px;">
          <div class="dialog-footer">
            <el-button cy-data="cancel-enviornment" @click="cancelEnv()">取消</el-button>
            <el-button cy-data="save-enviornment" type="primary" @click="onSubmit('form')">保存</el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { projectList } from '@/api/projects'
import { createEnv, updateEnv, envDetail } from '@/api/evns'
export default {
  props: {
    eid: {
      type: Number,
      default: 1
    }
  },
  data() {
    return {
      showStatus: true,
      showTitle: '',
      form: {
        name: '',
        project_id: '',
        env: '',
        browser: '',
        base_url: ''
      },
      inResize: true,
      projectOption: []
    }
  },
  created() {
    if (this.eid === 0) {
      this.showTitle = '创建环境'
    } else {
      this.showTitle = '编辑环境'
      this.getEnv()
    }
  },
  mounted() {
    this.projectList()
  },
  methods: {
    // 创建&编辑环境
    onSubmit(formNmame) {
      this.$refs[formNmame].validate(valid => {
        if (valid) {
          if (this.eid === 0) {
            createEnv(this.form).then(resp => {
              if (resp.success === true) {
                this.$message.success('创建成功！')
                this.cancelEnv()
              } else { this.$message.error('创建失败！') }
            })
          } else {
            updateEnv(this.eid, this.form).then(resp => {
              if (resp.success === true) {
                this.$message.success('更新成功！')
                this.cancelEnv()
              } else {
                this.$message.error('更新失败！')
              }
            })
          }
        } else {
          return false
        }
      })
    },
    // 获取环境信息
    async getEnv() {
      const resp = await envDetail(this.eid)
      if (resp.success === true) {
        this.form = resp.data
        this.form.project_id = resp.data.project
      } else {
        this.$message.error(resp.error.message)
      }
    },
    // 关闭dialog
    cancelEnv() {
      this.$emit('cancel', {})
    },
    // 获取项目列表
    async projectList() {
      const resp = await projectList(this.req)
      if (resp.success === true) {
        for (let i = 0; i < resp.items.length; i++) {
          this.projectOption.push({
            value: resp.items[i].id,
            label: resp.items[i].name
          })
        }
        // this.$message.success("查询成功！")
      } else {
        this.$message.error('查询失败！')
      }
    }
  }
}
</script>

<style scoped>
.dialog-footer {
    float: right;
}
</style>
