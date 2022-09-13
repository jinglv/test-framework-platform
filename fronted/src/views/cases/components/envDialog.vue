<template>
  <el-dialog
    :visible.sync="dialogVisible"
    width="500px"
    :before-close="closeDialog"
  >
    <el-form
      ref="ruleForm"
      :model="envForm"
      label-width="100px"
      class="demo-ruleForm"
    >
      <el-form-item label="环境名称" prop="name">
        <el-input v-model="envForm.name" />
      </el-form-item>
      <el-form-item label="环境" prop="env">
        <el-input v-model="envForm.env" />
      </el-form-item>
      <el-form-item label="浏览器" prop="browser">
        <el-input v-model="envForm.browser" />
      </el-form-item>
      <el-form-item label="地址" prop="base_url">
        <el-input v-model="envForm.base_url" />
      </el-form-item>
      <el-form-item style="text-align: right">
        <el-button @click="closeDialog">取消</el-button>
        <el-button
          type="primary"
          @click="submitEnv()"
        >确定</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script>
import { createEnv } from '@/api/evns'

export default {
  name: 'EnvDialog',
  components: {},
  props: {
    pid: {
      type: Number,
      default: 1
    }
  },
  data() {
    return {
      dialogVisible: true,
      updateURL: '',
      envForm: {
        name: '',
        env: '',
        browser: '',
        base_url: ''
      }
    }
  },
  mounted() {
  },
  methods: {
    closeDialog() {
      console.log('closeDialog')
      this.$emit('cancel', {})
    },
    submitEnv() {
      const req = {
        name: this.envForm.name,
        project_id: this.pid,
        env: this.envForm.env,
        browser: this.envForm.browser,
        base_url: this.envForm.base_url
      }
      createEnv(req).then((resp) => {
        if (resp.success === true) {
          // 创建成功，关闭弹窗
          this.closeDialog()
          this.$message.success('项目创建成功！')
        } else {
          this.$message.error(resp.error.message)
        }
      })
    }
  }
}
</script>
