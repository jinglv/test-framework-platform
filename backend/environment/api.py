# Create your views here.
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from backend.api_response import response, model_to_dict, Error
from backend.pagination import CustomPagination
from environment.env_schema import EnvIn, EnvListOut
from environment.models import Envs
from projects.models import Project

router = Router(tags=["env"])


@router.post('/create')
def create_env(request, env: EnvIn):
    """
    创建环境
    """
    get_object_or_404(Project, pk=env.project_id)
    env_obj = Envs.objects.create(
        name=env.name,
        project_id=env.project_id,
        env=env.env,
        browser=env.browser,
        base_url=env.base_url)
    return response(data=model_to_dict(env_obj))


@router.get('/{env_id}/')
def get_env(request, env_id: int):
    """
    获取环境
    """
    try:
        env = Envs.objects.get(id=env_id)
    except Envs.DoesNotExist:
        return response(error=Error.ENV_IS_NULL)
    return response(data=model_to_dict(env))


@router.get('/{project_id}/list')
def get_env_list_for_project(request, project_id: int):
    """
    获取环境列表
    """
    envs = Envs.objects.filter(project_id=project_id).all()
    env_list = []
    for env in envs:
        env_list.append(model_to_dict(env))
    return response(data=env_list)


@router.delete('/{env_id}/')
def delete_env(request, env_id: int):
    """
    删除环境
    """
    try:
        env = Envs.objects.get(id=env_id)
        env.delete()
    except Envs.DoesNotExist:
        return response(error=Error.ENV_IS_NULL)

    return response()


@router.put('/{env_id}/')
def update_env(request, env_id: int, env: EnvIn):
    """
    更新环境
    """
    try:
        env_obj = Envs.objects.get(id=env_id)
        env_obj.name = env.name
        env_obj.project_id = env.project_id
        env_obj.env = env.env
        env_obj.browser = env.browser
        env_obj.base_url = env.base_url
        env_obj.save()
    except Envs.DoesNotExist:
        return response(error=Error.ENV_IS_NULL)
    return response()


@router.get('/list', response=List[EnvListOut])
@paginate(CustomPagination)
def get_env_list(request):
    """
    获取所有环境列表
    """
    envs = Envs.objects.all()
    result = []
    env_dict = {}
    for env in envs:
        project = get_object_or_404(Project, pk=env.project_id, is_delete=False)
        project_name = project.name
        env_dict = {
            'id': env.id,
            'name': env.name,
            'project_name': project_name,
            'env': env.env,
            'browser': env.browser,
            'base_url': env.base_url,
            'update_time': env.update_time
        }
        result.append(env_dict)
    return result
