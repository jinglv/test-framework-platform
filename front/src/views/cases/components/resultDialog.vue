<template>
  <span>
    <el-tabs v-model="activeName" style="margin-left: 5px; margin-right: 5px;">
      <el-tab-pane label="用例信息" name="first">
        <el-form ref="resultData" :model="resultData" label-position="right" label-width="100px">
          <el-form-item label="报告名称:">
            {{ resultData.name }}
          </el-form-item>
          <el-form-item label="创建时间:">
            {{ resultData.create_time }}
          </el-form-item>
          <el-form-item label="运行时长:">
            {{ resultData.run_time }} s
          </el-form-item>
          <el-form-item label="总数:">
            <el-tag>{{ resultData.tests }}</el-tag>
          </el-form-item>
          <el-form-item label="通过:">
            <el-tag type="success">{{ resultData.passed }}</el-tag>
          </el-form-item>
          <el-form-item label="跳过:">
            <el-tag type="info">{{ resultData.skipped }}</el-tag>
          </el-form-item>
          <el-form-item label="失败:">
            <el-tag type="warning">{{ resultData.failure }}</el-tag>
          </el-form-item>
          <el-form-item label="错误:">
            <el-tag type="danger">{{ resultData.error }}</el-tag>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="运行日志" name="second">
        <el-input
          v-model="resultData.system_out"
          type="textarea"
          :rows="32"
          placeholder="system out is null"
        />
      </el-tab-pane>
    </el-tabs>
  </span>
</template>

<script>
import { caseResult } from '@/api/cases'

export default {
  props: {
    cid: {
      type: Number,
      default: 1
    }
  },
  data() {
    return {
      drawer: true,
      activeName: 'first',
      resultData: {},
      reportData: ''
    }
  },
  created() {
    this.drawer = true
  },
  mounted() {
    this.initCaseResult()
  },
  methods: {
    // 查询用例结果
    async initCaseResult() {
      const resp = await caseResult(this.cid)
      if (resp.success === true) {
        this.resultData = resp.data
        this.reportData = resp.data.system_out
      } else {
        this.$message.error('获取结果失败')
      }
    },
    // 关闭dialog
    cancelDialog() {
      this.$emit('cancel', {})
    }
  }
}
</script>

  <style scoped>
  .dialog-footer {
    float: right;
  }
  </style>
