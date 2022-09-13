<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="500px"
    :before-close="closeDialog"
  >
    <el-form
      v-if="title == 'detail'"
      ref="ruleForm"
      :model="projectForm"
      :rules="rules"
      label-width="100px"
      class="demo-ruleForm"
    >
      <el-form-item label="项目名称" prop="name">{{
        projectForm.name
      }}</el-form-item>
      <el-form-item
        label="Git项目名称"
        prop="git_name"
      >{{ projectForm.git_name }}
      </el-form-item>
      <el-form-item
        label="Git项目地址"
        prop="git_address"
      >{{ projectForm.git_address }}
      </el-form-item>
      <el-form-item
        label="项目描述"
        prop="desc"
      >{{ projectForm.describe }}
      </el-form-item>
      <el-form-item label="图片" prop="image">
        <div id="image">
          <el-image
            style="width: 100px; height: 100px"
            :src="imageUrl"
          />
        </div>
      </el-form-item>
      <el-form-item style="text-align: right">
        <el-button @click="closeDialog">返回</el-button>
      </el-form-item>
    </el-form>
    <el-form
      v-if="title != 'detail'"
      ref="ruleForm"
      :model="projectForm"
      :rules="rules"
      label-width="100px"
      class="demo-ruleForm"
    >
      <el-form-item label="项目名称" prop="name">
        <el-input v-model="projectForm.name" />
      </el-form-item>
      <el-form-item label="Git项目名称" prop="git_name">
        <el-input v-model="projectForm.git_name" />
      </el-form-item>
      <el-form-item label="Git项目地址" prop="git_address">
        <el-input v-model="projectForm.git_address" />
      </el-form-item>
      <el-form-item label="项目描述" prop="desc">
        <el-input v-model="projectForm.describe" type="textarea" />
      </el-form-item>
      <el-form-item label="图片" prop="desc">
        <div id="image">
          <el-upload
            action="#"
            :before-upload="beforeUpload"
            list-type="picture-card"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :file-list="fileList"
          >
            <i class="el-icon-plus" />
          </el-upload>
          <el-dialog :visible.sync="imageVisible">
            <img width="100%" :src="imageUrl" alt="">
          </el-dialog>
        </div>
      </el-form-item>
      <el-form-item style="text-align: right">
        <el-button @click="closeDialog">取消</el-button>
        <el-button
          type="primary"
          @click="submitProject('ruleForm')"
        >确定</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>
<script>
import { getProject, createProject, updateProject, updateImage } from '@/api/projects'

export default {
  name: 'PorjectDialog',
  components: {},
  props: {
    title: {
      type: String,
      default: null
    },
    pid: {
      type: Number,
      default: 1
    }
  },
  data() {
    return {
      dialogVisible: true,
      showTitle: '',
      updateURL: '',
      projectForm: {
        name: '',
        git_name: '',
        git_address: '',
        describe: '',
        image: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入项目的名称', trigger: 'blur' }
        ]
      },
      fileList: [], // 现有图片列表
      imageUrl: '', // 图片路径
      imageVisible: false,
      disabled: false
    }
  },
  mounted() {
    if (this.title === 'create') {
      this.showTitle = '创建项目'
    } else if (this.title === 'detail') {
      this.showTitle = '项目详情'
      this.initProjectDetail()
    } else if (this.title === 'edit') {
      this.showTitle = '编辑项目'
      this.initProjectDetail()
    }
  },
  methods: {
    closeDialog() {
      console.log('closeDialog')
      this.$emit('cancel', {})
    },
    // 查询项目详情
    async initProjectDetail() {
      const resp = await getProject(this.pid)
      console.log('project info', resp)
      if (resp.success === true) {
        this.projectForm = resp.data
        this.fileList.push({
          name: resp.data.image,
          url: 'static/images/' + resp.data.image
        })
        this.imageUrl = 'static/images/' + resp.data.image
        this.$message.success('项目详情成功！')
      } else {
        this.$message.error('项目详情失败！')
      }
    },
    // 创建项目
    submitProject(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if (this.title === 'create') {
            createProject(this.projectForm).then((resp) => {
              if (resp.success === true) {
                // 创建成功，关闭弹窗
                this.closeDialog()
                this.$message.success('项目创建成功！')
              } else {
                this.$message.error(resp.error.message)
              }
            })
          } else if (this.title === 'edit') {
            updateProject(this.pid, this.projectForm).then((resp) => {
              if (resp.success === true) {
                this.closeDialog()
                this.$message.success('项目编辑成功！')
              } else {
                this.$message.error(resp.error.message)
              }
            })
          }
        } else {
          return false
        }
      })
    },
    // 删除图片
    handleRemove(file) {
      console.log('删除', file)
    },
    // 预览图片
    handlePreview(file, fileList) {
      console.log('上传成功', file, fileList)
      this.imageUrl = file.url
      this.imageVisible = true
    },
    // 上传文件
    async beforeUpload(file) {
      console.log('上传文件对象', file)
      const fb = new FormData()
      fb.append('file', file)
      const resp = await updateImage(fb)
      console.log('resp-->', resp)
      if (resp.success === true) {
        // 获取文件名
        this.projectForm.image = resp.data.name
        // 拼接静态文件路径，用于图片展示
        const imagePath = '/static/images/' + resp.data.name
        this.fileList.push({
          name: file.name,
          url: imagePath
        })
        this.$message.success('上传成功！')
      } else {
        console.log('上传失败', resp)
        this.$message.error(resp.error.message)
      }
    }
  }
}
</script>
