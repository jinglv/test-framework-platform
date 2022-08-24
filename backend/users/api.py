from django.contrib import auth
from django.contrib.auth.models import User
from django.db import transaction
from ninja import Router

from backend.api_response import response, Error
from users.user_schema import RegisterIn, LoginIn

router = Router(tags=["users"])


@router.post("/register", auth=None)
@transaction.atomic
def user_register(request, payload: RegisterIn):
    """
    用户注册接口
    - 用户名
    - 密码
    - 确认密码
    """
    # 判断两次密码输入是否一致
    if payload.password != payload.confirm_password:
        return response(error=Error.PWD_ERROR)
    try:
        User.objects.get_by_natural_key(payload.username)
    except User.DoesNotExist:
        pass
    else:
        return response(error=Error.USER_EXIST)
    user = User.objects.create_user(username=payload.username, password=payload.password)
    # 返回注册成功的用户信息
    registered_user = {
        "id": user.id,
        "username": user.username
    }
    return response(data=registered_user)


@router.post("/login", auth=None)
def user_login(request, payload: LoginIn):
    """
    用户登录
    """
    username = payload.username
    password = payload.password
    # 用户认证
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        # 会向django_session表 创建一条数据
        auth.login(request, user)
        # 获取最新的session信息
        token = request.session
        # 获取已登录的用户信息
        login_user_info = {
            "id": user.id,
            "username": user.username,
            "token": token.session_key
        }
        return response(data=login_user_info)
    else:
        return response(error=Error.USER_OR_PWD_ERROR)


@router.get("/info")
def user_info(request):
    """
    获取当前登录的用户信息
    """
    # 获取当前登录的用户信息
    user = auth.get_user(request)
    if user.username != "":
        users_info = {
            'id': user.id,
            'username': user.username,
            'avatar': 'avatar.jpeg'
        }
        return response(data=users_info)
    else:
        return response(error=Error.USER_NOT_LOGIN)


@router.delete("/logout")
def user_logout(request):
    """
    用户退出登录
    """
    # 用户退出登录
    auth.logout(request)
    return response()
