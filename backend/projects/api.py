# Create your views here.
import os
import subprocess
from typing import List

from django.db import transaction
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from backend.api_response import response, Error
from backend.pagination import CustomPagination
from backend.settings import BASE_DIR
from projects.models import Project
from projects.projects_schema import ProjectIn, ProjectListOut

router = Router(tags=["projects"])


@router.post("/create")
@transaction.atomic
def create_project(request, data: ProjectIn):
    """
    创建项目
    """
    project = Project.objects.filter(name=data.name)
    if len(project) > 0:
        return response(error=Error.PROJECT_NAME_EXIST)
    # 设置项目默认图片
    if data.image == "":
        data.image = "default_project_image.jpeg"
    Project.objects.create(**data.dict())
    return response()


@router.get("/list", response=List[ProjectListOut])
@paginate(CustomPagination)
def project_list(request, **kwargs):
    """
    项目列表
    """
    return Project.objects.filter(is_delete=False).all()


@router.get("/{project_id}")
def project_detail(request, project_id: int):
    """
    获取项目详情
    """
    project_obj = get_object_or_404(Project, pk=project_id, is_delete=False)
    return response(data=model_to_dict(project_obj))


@router.put("/{project_id}")
@transaction.atomic
def project_update(request, project_id: int, payload: ProjectIn):
    """
    更新项目详情
    """
    project = get_object_or_404(Project, id=project_id)
    for attr, value in payload.dict().items():
        setattr(project, attr, value)
    project.save()
    return response()


@router.delete("/{project_id}")
@transaction.atomic
def project_delete(request, project_id: int):
    """
    项目删除
    """
    projects = get_object_or_404(Project, id=project_id)
    projects.is_delete = True
    projects.save()
    return response()


@router.get("/clone/{project_id}")
def project_clone(request, project_id: int):
    """
    克隆git项目到本地
    """
    project = get_object_or_404(Project, id=project_id)
    project_address_name = str(project.git_address).split('/')[-1][:-4]
    clone_project_path = os.path.join(BASE_DIR, "git_project")
    full_project_file = clone_project_path + '/' + project_address_name
    print(project_address_name)
    if os.path.exists(full_project_file):
        # git项目存在，进行拉取
        args = ["pull"]
        res = subprocess.check_call(['git'] + list(args), cwd=full_project_file)
        if res == 0:
            return response()
        else:
            return response(error=Error.PROJECT_PULL_ERROR)
    else:
        # git项目不存在，进行clone
        args = ["clone", project.git_address]
        res = subprocess.check_call(['git'] + list(args), cwd=clone_project_path)
        if res == 0:
            return response()
        else:
            return response(error=Error.PROJECT_ClONE_ERROR)
