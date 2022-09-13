from itertools import chain


class Error:
    """
    预定义错误码与错误信息
    """
    USER_OR_PWD_NULL = {"10010": "用户名或密码为空"}
    USER_OR_PWD_ERROR = {"10011": "用户名或密码错误"}
    PWD_ERROR = {"10012": "两次密码不一致"}
    USER_EXIST = {"10013": "用户名已被注册"}
    USER_NOT_LOGIN = {"10014": "用户未登录"}

    PROJECT_NAME_EXIST = {"10021": "项目名称已存在"}
    PROJECT_NOT_EXIST = {"10022": "项目不存在"}
    PROJECT_IS_DELETE = {"10023": "项目已删除"}
    IMAGE_SUFFIX_ERROR = {"10024": "上传图片格式错误"}
    IMAGE_SIZE_ERROR = {"10024": "图片大小不能超过2MB"}
    JSONPATH_ERROR = {"10025": "JsonPath未能匹配到值"}
    PROJECT_ClONE_ERROR = {"10026": "项目克隆失败"}
    PROJECT_PULL_ERROR = {"10027": "项目拉取失败"}
    PROJECT_DIR_NULL = {"10028": "本地项目目录不存在"}

    ENV_IS_NULL = {"10031": "环境为空"}
    MODULE_NO_EXIST = {"10032": "项目中模块不存在"}
    MODULE_IS_DELETE = {"10033": "项目模块已删除"}

    CASE_DIR_ERROR = {"10041": "测试用例地址不存在"}
    CASE_IS_DELETE = {"10042": "测试用例已删除"}
    CASE_EXTRACT_ERROR = {"10043": "提取器校验失败"}

    BASE_DATA_TYPE_ERROR = {"10051": "基础数据类型错误"}
    SCENE_DATA_TYPE_ERROR = {"10052": "场景数据类型错误"}
    DATA_TYPE_NAME_EXIST = {"10053": "数据类型名称已存在"}

    TASK_IS_DELETE = {"10061": "测试任务已删除"}
    CASE_NOT_EXIST = {"10062": "测试用例不存在"}


def model_to_dict(instance: object) -> dict:
    """
    对象转字典
    """
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        data[f.name] = f.value_from_object(instance)
    return data


def response(success: bool = True, error=None, data=None) -> dict:
    """
    定义统一返回格式
    """
    if error is None:
        error_code = ""
        error_msg = ""
    else:
        success = False
        error_code = list(error.keys())[0]
        error_msg = list(error.values())[0]

    if data is None:
        item = {}
    elif isinstance(data, dict):
        item = data
    elif isinstance(data, list):
        item = data
    elif isinstance(data, object):
        item = model_to_dict(data)
    else:
        item = {}

    resp_data = {
        "success": success,
        "error": {
            "code": error_code,
            "message": error_msg
        },
        "data": item
    }
    return resp_data
