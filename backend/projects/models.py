from django.db import models


class Project(models.Model):
    """
    项目管理表
    """
    name = models.CharField("名称", max_length=50, null=False)
    git_name = models.CharField("git项目名称", max_length=50, null=True, default="")
    git_address = models.CharField("git项目地址", max_length=200, null=True, default="")
    describe = models.TextField("描述", null=True, default="")
    image = models.CharField("图片", max_length=50, null=True)
    is_delete = models.BooleanField("状态", null=True, default=False)
    test_num = models.IntegerField("文件数", default=0)
    is_clone = models.IntegerField("是否克隆", default=0)  # 1-已克隆 0-未克隆
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
