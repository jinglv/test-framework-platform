from django.db import models

# Create your models here.
from projects.models import Project


class Envs(models.Model):
    """
    环境管理
    说明：
    * env = Seldom.env  # 指定当前运行环境 env=production/develop/test
    * browser = seldom.main(browser="xxx")  # web测试，指定当前运行的浏览器 xxx=chrome/firefox/edge
    * base_url = seldom.main(base_url="xxx")  # http接口测试：指定当前运行的URL xxx=http://www.httpbin.org
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=50, null=False)
    env = models.CharField("环境值", max_length=50, null=True, default="")
    browser = models.CharField("环境值", max_length=20, null=True, default="")
    base_url = models.CharField("URL", max_length=200, null=True, default="")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
