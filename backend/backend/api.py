from django.contrib.sessions.models import Session
from django.http import HttpRequest
from ninja import NinjaAPI
from ninja.security import HttpBearer

from cases.api import router as cases_router
from commons.api import router as commons_router
from environment.api import router as environment_router
from projects.api import router as projects_router
from users.api import router as users_router


class InvalidToken(Exception):
    """
    无效token异常，定义异常类型，无需内容
    """
    pass


class OverdueToken(Exception):
    """
    过期token异常，定义异常类型，无需内容
    """
    pass


class GlobalAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str):
        """
        自定义认证token处理
        """
        try:
            # 获取token（表django_session）
            Session.objects.get(pk=token)
            # session过期处理，后续进行
        except Session.DoesNotExist:
            raise InvalidToken
        else:
            return token


api = NinjaAPI(auth=GlobalAuth())


@api.exception_handler(InvalidToken)
def on_invalid_token(request, exc):
    """
    无效token返回
    """
    return api.create_response(request, {"detail": "Invalid token supplied"}, status=401)


@api.exception_handler(OverdueToken)
def in_overdue_token(request, exc):
    """
    过期token返回
    """
    return api.create_response(request, {"detail": "Overdue token supplied"}, status=401)


# tags users URI:/api/users/xxx
api.add_router("/users/", users_router)
# tags commons URI:/api/commons/xxx
api.add_router("/commons/", commons_router)
# tags projects URI:/api/projects/xxx
api.add_router("/projects/", projects_router)
# tags cases URI:/api/cases/xxx
api.add_router("/cases/", cases_router)
# tags environment URI:/api/env/xxx
api.add_router("/env/", environment_router)
# # tags modules URI:/api/modules/xxx
# api.add_router("/modules/", modules_router)
# # tags tasks URI:/api/tasks/xxx
# api.add_router("/tasks/", tasks_router)
# # tags datas URI:/api/datas/xxx
# api.add_router("/datas/", datas_router)
# # tags reports URI:/api/reports/xxx
# api.add_router("/reports/", reports_router)
# # tags reports URI:/api/interfaces/xxx
# api.add_router("/interfaces/", interfaces_router)
