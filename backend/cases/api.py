import os
import threading
import time

from django.shortcuts import get_object_or_404
from ninja import Router
from seldom import SeldomTestLoader, TestMainExtend
from seldom.utils import file

from backend.api_response import response, Error, model_to_dict
from backend.settings import BASE_DIR
from cases.cases_schema import RunCaseIn
from cases.models import TestCase, CaseResult
from cases.utils import thread_run_case
from projects.models import Project

router = Router(tags=["cases"])


@router.get("/sync")
def sync_cases(request, project_id: int):
    """
    同步项目用例
    """
    project_obj = get_object_or_404(Project, pk=project_id)
    # 开启收集测试用例
    SeldomTestLoader.collectCaseInfo = True
    # 项目本地目录
    project_name = project_obj.git_name
    git_local_dir = os.path.join(BASE_DIR, "git_project")
    project_local_dir = os.path.join(git_local_dir, project_name)

    # 把项目目录加到环境变量path
    file.add_to_path(project_local_dir)

    # test_dir = file.join(project_local_dir, project_name)
    if os.path.isdir(project_local_dir) is False:
        return response(error=Error.PROJECT_DIR_NULL)

    # 收集测试用例信息
    main_extend = TestMainExtend(path=project_local_dir)
    seldom_case = main_extend.collect_cases(json=False)

    cases = TestCase.objects.filter(project=project_obj)

    # 从seldom项目中找到新增的用例
    for seldom in seldom_case:
        for case in cases:
            if (seldom["file"] == case.file_name and seldom["class"]["name"] == case.class_name
                    and seldom["method"]["name"] == case.case_name):
                break
        else:
            TestCase.objects.create(
                project_id=project_id,
                file_name=seldom["file"].replace('\n', '').replace('\r', '').strip(),
                class_name=seldom["class"]["name"].replace('\n', '').replace('\r', '').strip(),
                class_doc=seldom["class"]["doc"].replace('\n', '').replace('\r', '').strip(),
                case_name=seldom["method"]["name"].replace('\n', '').replace('\r', '').strip(),
                case_doc=seldom["method"]["doc"].replace('\n', '').replace('\r', '').strip(),
            )
    # 从platform找出已删除的用例
    for case in cases:
        for seldom in seldom_case:
            if (case.file_name == seldom["file"]
                    and case.class_name == seldom["class"]["name"].replace('\n', '').replace('\r', '').strip()
                    and case.case_name == seldom["method"]["name"].replace('\n', '').replace('\r', '').strip()):
                break
        else:
            test_case = TestCase.objects.filter(project=project_obj, id=case.id)
            test_case.delete()
    return response()


@router.get("/{project_id}/files")
def get_project_files(request, project_id: int):
    """
    获取项目用例文件列表
    """
    cases = TestCase.objects.filter(project_id=project_id)
    case_number = len(cases)
    files = []
    files_name = []
    for case in cases:
        # 判断目录和文件
        if "." in case.file_name:
            # 分割文件名
            case_path = case.file_name.split('.')
        else:
            # 不能分割则是*.py文件
            case_path = [case.file_name + ".py"]
        # case_path[0]一级目录
        if case_path[0] not in files_name:
            files_name.append(case_path[0])
            if ".py" in case_path[0]:
                case_level_one = {
                    "label": case_path[0],
                    "full_name": case_path[0],
                    "is_leaf": 1,
                    "children": []
                }
            else:
                case_level_one = {
                    "label": case_path[0],
                    "full_name": case_path[0],
                    "is_leaf": 0,
                    "children": []
                }
            files.append(case_level_one)
    return response(data={"case_number": case_number, "files": files})


@router.get('/{project_id}/subdirectory')
def get_project_subdirectory(request, project_id: int, file_name: str):
    """
    获取子目录
    """
    all_cases = TestCase.objects.filter(project_id=project_id)
    files_name = []
    for case in all_cases:
        if case.file_name.startswith(file_name + ".") is True:
            if case.file_name[len(file_name + "."):] not in files_name:
                files_name.append(case.file_name[len(file_name + "."):])

    case_name = []
    dir_name = []
    for f_name in files_name:
        if "." in f_name:
            case_path = f_name.split('.')
            if case_path[0] not in dir_name:
                dir_name.append(case_path[0])
            else:
                continue
            case_level_two = {
                "label": case_path[0],
                "full_name": file_name + "." + case_path[0],
                "is_leaf": 0,
                "children": []
            }
        else:
            case_path = [f_name + ".py"]
            case_level_two = {
                "label": case_path[0],
                "full_name": file_name + "." + case_path[0],
                "is_leaf": 1,
                "children": []
            }
        case_name.append(case_level_two)
    return response(data=case_name)


@router.get('/{project_id}/cases')
def get_project_file_cases(request, project_id: int, file_name: str):
    """
    file_name存储全路径: test_dir.test_user.test_user_abnormal + '.py'
    获取文件下面的测试用例
    """
    # 如果是文件，直接取文件的类、方法
    if ".py" in file_name:
        file_cases = TestCase.objects.filter(
            project_id=project_id,
            file_name=file_name[0:-3]
        )
        case_list = []
        for case in file_cases:
            case_list.append(model_to_dict(case))
        return response(data=case_list)
    return response()


@router.post('/{case_id}/running')
def running_case(request, case_id: int, env: RunCaseIn):
    """
    运行测试用例
    """
    # 运行环境
    env = env.env
    case = get_object_or_404(TestCase, pk=case_id)
    case.status = 1
    case.save()

    case_info = [{
        "file": case.file_name,
        "class": {
            "name": case.class_name,
            "doc": case.class_doc
        },
        "method": {
            "name": case.case_name,
            "doc": case.case_doc
        }
    }]

    # 项目目录添加环境变量
    project = Project.objects.get(id=case.project_id)
    file.add_to_path(project.git_address)

    # 项目相关目录
    project_name = project.git_name
    project_address = file.join(BASE_DIR, "git_project", project_name)
    print(project_address)
    # project_case_dir = file.join(project_address, project.case_dir)

    # 判断目录是否存在
    if os.path.exists(project_address) is False:
        return response(error=Error.CASE_DIR_ERROR)

    # 添加环境变量
    file.add_to_path(project_address)

    # 定义报告
    report_name = f'{str(time.time()).split(".")[0]}.xml'
    # 丢给线程执行用例
    threads = []
    t = threading.Thread(target=thread_run_case, args=(project_address, case_info, report_name, case.id, env))
    threads.append(t)
    for t in threads:
        t.start()

    return response()


@router.get('/{case_id}/result')
def get_case_result(request, case_id: int):
    """
    获取测试用例执行结果
    """
    results = CaseResult.objects.filter(case_id=case_id).order_by("-create_time")
    if len(results) == 0:
        result = []
    else:
        result = results[0]
    return response(data=result)
